package fi.oulu.smartshophelper.ui;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.StatusLine;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.entity.AbstractHttpEntity;
import org.apache.http.entity.ByteArrayEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicHeader;
import org.apache.http.protocol.HTTP;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

import fi.oulu.smartshophelper.R;
import fi.oulu.smartshophelper.model.Item;
import fi.oulu.smartshophelper.model.Store;

/**
 * Created by researcher on 30/06/15.
 */
public class UpdatePriceActivity extends Activity {

    private ListView listView;
    private ArrayAdapter<Store> arrayAdapter;
    private List<Store> stores;
    private Item item;
    private Store store;

    private String IP;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_update_price);

        SharedPreferences prefs = getSharedPreferences("fi.oulu.smartshophelper",MODE_PRIVATE);
        IP = prefs.getString("ip_address","");

        item = (Item) getIntent().getSerializableExtra("item");

        ((TextView) findViewById(R.id.update_title)).setText(item.getName());
        stores = new ArrayList<>();

        listView = (ListView) findViewById(R.id.stores_list);
        arrayAdapter = new ArrayAdapter<Store>(this,R.layout.store_row, R.id.tv_store,stores);
        listView.setEmptyView(findViewById(R.id.loading_view));
        listView.setAdapter(arrayAdapter);
        listView.setChoiceMode(ListView.CHOICE_MODE_SINGLE);

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                listView.setItemChecked(position, true);
            }
        });

        ((ImageButton)findViewById(R.id.back_btn)).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        ((Button)findViewById(R.id.btn_update_price)).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(listView.getCheckedItemCount()>0)
                {
                    double price;
                    store = arrayAdapter.getItem(listView.getCheckedItemPosition());
                    try
                    {
                        price = Double.parseDouble(((EditText)findViewById(R.id.edt_new_price)).getText().toString().trim());
                    }
                    catch (Exception e)
                    {
                        Toast.makeText(getApplicationContext(),"Plase input a valid price",Toast.LENGTH_SHORT).show();
                        return;
                    }
                    ((Button)findViewById(R.id.btn_update_price)).setText("Updating Price...");
                    new UpdatePriceTask(store.getStore_id(),price,item.getId()).execute();
                }
            }
        });

        new StoresTask().execute();
    }

    private void refreshView(List<Store> newStores)
    {
        stores.clear();

        if(newStores!= null)
        {
            stores.addAll(newStores);
        }

        arrayAdapter.notifyDataSetChanged();
    }

    private void showResult(Boolean updated)
    {
        ((Button)findViewById(R.id.btn_update_price)).setText("Update Price");
        ((Button)findViewById(R.id.btn_update_price)).setEnabled(false);
        listView.setEnabled(false);
        ((EditText)findViewById(R.id.edt_new_price)).setEnabled(false);

        if(updated)
        {
            Toast.makeText(this,"The "+item.getName()+"'s price was updated for "+store.getName(),Toast.LENGTH_SHORT).show();
        }
        else
        {
            Toast.makeText(this,"Error updating price of the item",Toast.LENGTH_SHORT).show();
        }
    }

    private class StoresTask extends AsyncTask<Void, Void, List<Store>> {

        @Override
        protected ArrayList<Store> doInBackground(Void... params) {
            HttpClient client = new DefaultHttpClient();
            String result;
            Log.d("Task", "started");
            String URL = "http://"+IP+":5000";
            ArrayList<Store> thisStores = new ArrayList<>();

            //GET STORES
            try {
                StringBuilder builder = new StringBuilder();
                HttpGet storesGet = new HttpGet(URL + "/shop/api/stores?" +
                        "radius=10000000000");
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

                    for (int i = 0; i < jsonArrayStores.length(); i++) {
                        JSONObject jsonObjectStore = jsonArrayStores.getJSONObject(i);
                        double distance = jsonObjectStore.getDouble("distance");
                        String store_uri = jsonObjectStore.getString("href");
                        Store store = new Store(store_uri, distance);
                        thisStores.add(store);
                    }
                } else {
                    Log.e("Getter", "Failed to get stores");
                    return null;
                }
            } catch (Exception e) {
                Log.e("Error posting message", "HttpGet failed stores");
                Log.e("Error message", e.getMessage());
                return null;
            }

            for (int i = 0; i < thisStores.size(); i++) {
                Store thisStore = thisStores.get(i);
                try {
                    StringBuilder builder = new StringBuilder();
                    HttpGet storesGet = new HttpGet(URL + thisStore.getStore_uri());
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
                    } else {
                        Log.e("Getter", "Failed to get stores");
                        return null;
                    }
                } catch (Exception e) {
                    Log.e("Error posting message", "HttpGet failed stores");
                    Log.e("Error message", e.getMessage());
                    return null;
                }
            }

            return thisStores;
        }

        @Override
        protected void onPostExecute(List<Store> stores) {
            refreshView(stores);
        }
    }

    private class UpdatePriceTask extends AsyncTask<Void, Void, Boolean> {

        private String store_id;
        private double price;
        private String item_id;

        public UpdatePriceTask(String store_id, double price, String item_id) {
            this.store_id = store_id;
            this.price = price;
            this.item_id = item_id;
        }

        @Override
        protected Boolean doInBackground(Void... params) {
            HttpClient client = new DefaultHttpClient();
            String result;
            Log.d("Task", "started");
            String URL = "http://"+IP+":5000";
            ArrayList<Store> thisStores = new ArrayList<>();

            //GET STORES
            try {
                StringBuilder builder = new StringBuilder();
                HttpPut pricePut = new HttpPut(URL + "/shop/api/items/"+item_id+"/");

                JSONObject jsonObject = new JSONObject();
                jsonObject.put("price",price);
                jsonObject.put("store_id",store_id);

                AbstractHttpEntity entity = new ByteArrayEntity(jsonObject.toString().getBytes("UTF8"));
                entity.setContentType(new BasicHeader(HTTP.CONTENT_TYPE, "application/json"));
                pricePut.setEntity(entity);

                HttpResponse response = client.execute(pricePut);

                StatusLine statusLine = response.getStatusLine();
                int statusCode = statusLine.getStatusCode();
                if (statusCode == 200) {
                    return true;
                } else {
                    Log.e("Getter", "Failed to get stores");
                    return false;
                }
            } catch (Exception e) {
                Log.e("Error posting message", "HttpPut failed stores");
                Log.e("Error message", e.getMessage());
                return false;
            }
        }

        @Override
        protected void onPostExecute(Boolean aBoolean) {
            showResult(aBoolean);
        }
    }
}
