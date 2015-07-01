package fi.oulu.smartshophelper.ui;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.TextView;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.StatusLine;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;

import fi.oulu.smartshophelper.R;
import fi.oulu.smartshophelper.db.CartDataSource;
import fi.oulu.smartshophelper.model.CartItem;
import fi.oulu.smartshophelper.model.Category;
import fi.oulu.smartshophelper.model.Item;
import fi.oulu.smartshophelper.model.Price;
import fi.oulu.smartshophelper.model.Store;

/**
 * Created by researcher on 01/07/15.
 */
public class SearchResultActivity extends Activity implements LocationListener {

    private static final long MIN_TIME = 400;
    private static final float MIN_DISTANCE = 100;

    private ListView listView;
    private List<ResultItem> items;
    private SearchResultAdapter searchResultAdapter;

    private TextView tv_total;
    private TextView tv_low_savings;
    private TextView tv_high_savings;

    private int distance;

    private LocationManager locationManager;

    private double latitude;
    private double longitude;

    private boolean haveLocation;
    private boolean haveCart;

    private List<CartItem> cartItems;

    private String IP;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search_result);
        SharedPreferences prefs = getSharedPreferences("fi.oulu.smartshophelper",MODE_PRIVATE);
        IP = prefs.getString("ip_address","");

        distance = getIntent().getIntExtra("distance",-1);
        items = new ArrayList<>();
        haveLocation = false;
        haveCart = false;

        listView = (ListView) findViewById(R.id.list_view);
        tv_total = (TextView) findViewById(R.id.tv_total);
        tv_low_savings = (TextView) findViewById(R.id.tv_low_savings);
        tv_high_savings = (TextView) findViewById(R.id.tv_high_savings);

        searchResultAdapter = new SearchResultAdapter(this, items);

        listView.setAdapter(searchResultAdapter);
        listView.setEmptyView(findViewById(R.id.loading_view));

        locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        locationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, MIN_TIME, MIN_DISTANCE, this);
        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, MIN_TIME, MIN_DISTANCE, this);

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                ResultItem item = searchResultAdapter.getItem(position);
                if (item instanceof Header) {
                    Header header = (Header) item;
                    Intent intent = new Intent(getApplicationContext(), StoreSummaryActivity.class);
                    intent.putExtra("store", header.getStore());
                    startActivity(intent);
                }
            }
        });

        ((ImageButton)findViewById(R.id.back_btn)).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        getCart();

    }

    @Override
    public void onLocationChanged(Location location) {
        if(location.getAccuracy()<100) {
            latitude = location.getLatitude();
            longitude = location.getLongitude();
            locationManager.removeUpdates(this);


            if(haveCart)
            {
                new ResultTask(cartItems).execute();
            }
            else
            {
                haveLocation = true;
            }

        }
    }

    @Override
    public void onStatusChanged(String provider, int status, Bundle extras) {

    }

    @Override
    public void onProviderEnabled(String provider) {

    }

    @Override
    public void onProviderDisabled(String provider) {

    }

    private void getCart(){
        CartDataSource cartDataSource = new CartDataSource(this);
        cartDataSource.open();
        cartItems = cartDataSource.getAllItems();

        cartDataSource.close();

        if(haveLocation)
        {
            new ResultTask(cartItems).execute();
        }
        else
        {
            haveCart = true;
        }
    }

    private void refreshView(List<Store> theStores)
    {
        DecimalFormat dec = new DecimalFormat("#.00 EUR");
        double total = 0;
        double max = 0;
        double min = 0;

        items.clear();
        for(int i = 0; i<theStores.size();i++)
        {
            Store store = theStores.get(i);
            if(store.getItems()!=null&&store.getItems().size()>0)
            {
                items.add(new Header(store));
                for(int j = 0; j<store.getItems().size();j++)
                {
                    Price item = store.getItems().get(j);
                    total += (item.getQuantity()*item.getPrice());
                    items.add(new ListItem(item.getName(),item.getQuantity()+"",dec.format((item.getQuantity()*item.getPrice()))));
                }
            }
            if(store.getTotalPrice() > max)
            {
                max = store.getTotalPrice();
            }

            if(min==0||store.getTotalPrice() < min)
            {
                min = store.getTotalPrice();
            }
        }

        tv_total.setText(dec.format(total));
        double min_dif = min-total;
        double max_dif = max-total;
        if(min_dif<0)
            min_dif=0;
        if(max_dif<0)
            max_dif=0;
        tv_high_savings.setText(dec.format(max_dif));
        if(min_dif==0)
        {
            tv_low_savings.setText("");
        }
        else
        {
            tv_low_savings.setText(dec.format(min_dif));
        }
        findViewById(R.id.loading_view).setVisibility(View.GONE);
        listView.setEmptyView(findViewById(R.id.empty_view));
        searchResultAdapter.notifyDataSetChanged();
    }

    private class ResultTask extends AsyncTask<Void, Void, List<Store>>
    {

        private List<CartItem> items;

        public ResultTask(List<CartItem> items)
        {
            this.items = items;
        }

        @Override
        protected ArrayList<Store> doInBackground(Void... params) {
            HttpClient client = new DefaultHttpClient();
            String result;
            Log.d("Task", "started");
            String URL = "http://"+IP+":5000";
            ArrayList<Store> stores = new ArrayList<>();

            //GET STORES
            try
            {
                StringBuilder builder = new StringBuilder();
                HttpGet storesGet = new HttpGet(URL+"/shop/api/stores?"+
                        "radius="+distance+
                        "&latitude="+latitude+
                        "&longitude="+longitude);
                HttpResponse response = client.execute(storesGet);

                StatusLine statusLine = response.getStatusLine();
                int statusCode = statusLine.getStatusCode();
                if (statusCode == 200) {
                    HttpEntity entity = response.getEntity();
                    InputStream content = entity.getContent();
                    BufferedReader reader = new BufferedReader(
                            new InputStreamReader(content));
                    String line;
                    while ((line = reader.readLine()) != null) {
                        builder.append(line);
                    }
                    Log.v("Getter", "Your data: " + builder.toString());
                    result = builder.toString();

                    JSONObject jsonStores = new JSONObject(result);
                    JSONArray jsonArrayStores = jsonStores.getJSONArray("stores");

                    for(int i = 0; i<jsonArrayStores.length();i++)
                    {
                        JSONObject jsonObjectStore = jsonArrayStores.getJSONObject(i);
                        double distance = jsonObjectStore.getDouble("distance");
                        String store_uri = jsonObjectStore.getString("href");
                        Store store = new Store(store_uri, distance);
                        stores.add(store);
                    }
                }
                else
                {
                    Log.e("Getter", "Failed to get stores");
                    return null;
                }
            }
            catch(Exception e)
            {
                Log.e("Error posting message", "HttpGet failed stores");
                Log.e("Error message",e.getMessage());
                return null;
            }

            for(int i = 0; i<stores.size();i++)
            {
                Store thisStore = stores.get(i);
                try
                {
                    StringBuilder builder = new StringBuilder();
                    HttpGet storesGet = new HttpGet(URL+thisStore.getStore_uri());
                    HttpResponse response = client.execute(storesGet);

                    StatusLine statusLine = response.getStatusLine();
                    int statusCode = statusLine.getStatusCode();
                    if (statusCode == 200) {
                        HttpEntity entity = response.getEntity();
                        InputStream content = entity.getContent();
                        BufferedReader reader = new BufferedReader(
                                new InputStreamReader(content));
                        String line;
                        while ((line = reader.readLine()) != null) {
                            builder.append(line);
                        }
                        Log.v("Getter", "Your data: " + builder.toString());
                        result = builder.toString();

                        JSONObject jsonStores = new JSONObject(result);
                        JSONObject jsonStore = jsonStores.getJSONObject("store");

                        String store_id = jsonStore.getString("store_id");
                        String address = jsonStore.getString("address");
                        String name = jsonStore.getString("name");
                        double theLatitude = jsonStore.getDouble("latitude");
                        double theLongitude = jsonStore.getDouble("longitude");

                        thisStore.fill(name, address, theLatitude, theLongitude, store_id);
                    }
                    else
                    {
                        Log.e("Getter", "Failed to get stores");
                        return null;
                    }
                }
                catch(Exception e)
                {
                    Log.e("Error posting message", "HttpGet failed stores");
                    Log.e("Error message",e.getMessage());
                    return null;
                }
            }


            //GET PRICES



            for(int i = 0; i<items.size();i++)
            {
                ArrayList<Price> resultPrices = new ArrayList<>();
                try
                {
                    StringBuilder builder = new StringBuilder();
                    HttpGet request = new HttpGet(URL+items.get(i).getPrice_uri());
                    HttpResponse response = client.execute(request);

                    StatusLine statusLine = response.getStatusLine();
                    int statusCode = statusLine.getStatusCode();
                    if (statusCode == 200) {
                        HttpEntity entity = response.getEntity();
                        InputStream content = entity.getContent();
                        BufferedReader reader = new BufferedReader(
                                new InputStreamReader(content));
                        String line;
                        while ((line = reader.readLine()) != null) {
                            builder.append(line);
                        }
                        Log.v("Getter", "Your data: " + builder.toString());
                        result = builder.toString();

                        JSONArray jsonArrayPrices = new JSONArray(result);

                        for(int j = 0; j<jsonArrayPrices.length();j++)
                        {
                            JSONObject jsonItem = jsonArrayPrices.getJSONObject(j);

                            try
                            {
                                long timestamp = jsonItem.getLong("timestamp");
                                double price = jsonItem.getDouble("price");
                                String store_uri = jsonItem.getString("store_uri");

                                resultPrices.add(new Price(price,timestamp,store_uri, items.get(i).getId(), items.get(i).getName(),items.get(i).getQuantity()));
                            }
                            catch (Exception e){
                                resultPrices = null;
                            }

                        }
                        items.get(i).setPrices(resultPrices);

                    }
                    else
                    {
                        Log.e("Getter", "Failed to get items");
                    }
                }
                catch(Exception e)
                {
                    Log.e("Error posting message", "HttpGet failed");
                    Log.e("Error message",e.getMessage());
                }
            }

            for(int i = 0; i<stores.size();i++)
            {
                Store store = stores.get(i);
                for(int j = 0; j<items.size();j++)
                {
                    CartItem item = items.get(j);
                    ArrayList<Price> itemsPrices = item.getPrices();
                    for(int k = 0; k<itemsPrices.size();k++)
                    {
                        Price price = itemsPrices.get(k);
                        if(price.getStore_uri().trim().equals(store.getStore_uri().trim()))
                        {
                            store.addItem(price);
                        }
                    }
                }
            }

            for(int i = 0; i<stores.size();i++)
            {
                Store store = stores.get(i);
                ArrayList<Price> storesItems = store.getItems();
                for(int j = 0; j<storesItems.size();j++)
                {
                    Price storeItem = storesItems.get(j);
                    for(int k = 0; k<stores.size();k++)
                    {
                        if(i != k)
                        {
                            Store compareStore = stores.get(k);
                            ArrayList<Price> compareSoresItems = compareStore.getItems();
                            outerloop:
                            for(int h = 0; h<compareSoresItems.size();h++)
                            {
                                Price compareItem = compareSoresItems.get(h);
                                if(storeItem.getItem_id().equals(compareItem.getItem_id()))
                                {
                                    if(storeItem.getPrice()<compareItem.getPrice())
                                    {
                                        compareStore.deleteItem(compareItem);
                                        break outerloop;
                                    }
                                }
                            }

                        }
                    }
                }
            }

            return stores;
        }

        @Override
        protected void onPostExecute(List<Store> theStores) {
            refreshView(theStores);
        }
    }
}
