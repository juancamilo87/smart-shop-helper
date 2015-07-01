package fi.oulu.smartshophelper.ui;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.StatusLine;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONArray;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;

import fi.oulu.smartshophelper.R;
import fi.oulu.smartshophelper.db.CartDataSource;
import fi.oulu.smartshophelper.model.CartItem;
import fi.oulu.smartshophelper.model.Category;
import fi.oulu.smartshophelper.model.Item;

/**
 * Created by researcher on 30/06/15.
 */
public class ItemsActivity extends Activity {

    private ListView listView;
    private ArrayAdapter<Item> arrayAdapter;
    private ArrayList<Item> items;
    private TextView emptyView;
    private TextView title;
    private Category category;

    private CartDataSource cartDataSource;


    private String IP;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);


        SharedPreferences prefs = getSharedPreferences("fi.oulu.smartshophelper",MODE_PRIVATE);
        IP = prefs.getString("ip_address","");
        setContentView(R.layout.activity_items);

        listView = (ListView) findViewById(R.id.list_view);
        emptyView = (TextView) findViewById(R.id.empty_view);
        title = (TextView) findViewById(R.id.items_title);
        category = (Category) getIntent().getSerializableExtra("category");
        title.setText(category.toString());

        items = new ArrayList<>();
        arrayAdapter = new ArrayAdapter<Item>(this, android.R.layout.simple_list_item_1, items);

        listView.setAdapter(arrayAdapter);
        listView.setEmptyView(emptyView);

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Item item = arrayAdapter.getItem(position);

                showDialog(item);
            }
        });

        ((ImageButton)findViewById(R.id.back_btn)).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        ((ImageButton)findViewById(R.id.cart_btn)).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getApplicationContext(), CartActivity.class);
                startActivity(intent);
            }
        });

        new ItemsTaks(category.getItems()).execute();
    }

    private void getItems(ArrayList<Item> newItems) {

        items.clear();

        if(newItems!=null)
        {
            items.addAll(newItems);
        }
        if(items.size()==0)
        {
            emptyView.setText("No items available");
        }

        arrayAdapter.notifyDataSetChanged();
    }

    private void showDialog(final Item item)
    {
        AlertDialog.Builder builderSingle = new AlertDialog.Builder(
                ItemsActivity.this);
        LayoutInflater inflater = getLayoutInflater();
        View titleView = inflater.inflate(R.layout.item_dialog_title, null);
        ((TextView)titleView.findViewById(R.id.dialog_item_title)).setText(item.toString());
        builderSingle.setCustomTitle(titleView);

        final ArrayAdapter<String> arrayAdapter = new ArrayAdapter<String>(
                ItemsActivity.this,
                R.layout.list_cell);
        arrayAdapter.add("Add");
        //arrayAdapter.add("Delete");
        arrayAdapter.add("Update Price");

        builderSingle.setAdapter(arrayAdapter,
                new DialogInterface.OnClickListener() {

                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        String strName = arrayAdapter.getItem(which);
                        Intent intent;
                        switch (strName) {
                            case "Add":
                                addItemToCart(item);
                                break;
                            case "Delete":
                                deleteItem(item);
                                break;
                            case "Update Price":
                                intent = new Intent(getApplicationContext(), UpdatePriceActivity.class);
                                intent.putExtra("item", item);
                                startActivity(intent);
                                break;
                            default:
                                intent = new Intent();
                                break;
                        }
                        dialog.dismiss();
                    }
                });
        builderSingle.show();
    }

    private void addItemToCart(Item item)
    {
        if(cartDataSource==null)
        {
            cartDataSource = new CartDataSource(this);
        }
        cartDataSource.open();
        CartItem cartItem = cartDataSource.addItem(item);
        cartDataSource.close();
        if(cartItem==null)
        {
            Toast.makeText(this,"There was an error adding the item",Toast.LENGTH_SHORT).show();
        }
        else
        {
            Toast.makeText(this,"The item "+cartItem.getName()+" was added to the cart",Toast.LENGTH_SHORT).show();
        }
    }

    private void deleteItem(Item item)
    {
        if(cartDataSource==null)
        {
            cartDataSource = new CartDataSource(this);
        }
        cartDataSource.open();
        cartDataSource.deleteItem(item);
        cartDataSource.close();
    }

    private class ItemsTaks extends AsyncTask<Void, Void, ArrayList<Item>>
    {

        private ArrayList<Item> items;

        public ItemsTaks(ArrayList<Item> items)
        {
            this.items = items;
        }

        @Override
        protected ArrayList<Item> doInBackground(Void... params) {
            HttpClient client = new DefaultHttpClient();
            String result;
            Log.d("Task", "started");
            String URL = "http://"+IP+":5000";
            ArrayList<Item> resultItems = new ArrayList<>();

            for(int i = 0; i<items.size();i++)
            {
                try
                {
                    StringBuilder builder = new StringBuilder();
                    HttpGet request = new HttpGet(URL+items.get(i).getItem_uri());
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

                        JSONObject jsonItem = new JSONObject(result);

                        String item_id = jsonItem.getString("item_id");
                        String prices_uri = jsonItem.getString("prices_uri");
                        String name = jsonItem.getString("name");
                        String description = jsonItem.getString("description");

                        resultItems.add(new Item(name,prices_uri,description,item_id));

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

            return resultItems;
        }

        @Override
        protected void onPostExecute(ArrayList<Item> newItems) {
            getItems(newItems);
        }
    }
}
