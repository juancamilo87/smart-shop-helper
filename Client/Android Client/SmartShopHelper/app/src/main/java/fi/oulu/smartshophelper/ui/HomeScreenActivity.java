package fi.oulu.smartshophelper.ui;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.TextView;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.StatusLine;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
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
import java.lang.reflect.Array;
import java.util.ArrayList;

import fi.oulu.smartshophelper.R;
import fi.oulu.smartshophelper.model.Category;
import fi.oulu.smartshophelper.model.Item;

/**
 * Created by researcher on 30/06/15.
 */
public class HomeScreenActivity extends Activity{

    private ListView listView;
    private ArrayAdapter<Category> arrayAdapter;
    private ArrayList<Category> categories;
    private TextView emptyView;

    private String IP;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_home_screen);

        SharedPreferences prefs = getSharedPreferences("fi.oulu.smartshophelper",MODE_PRIVATE);
        IP = prefs.getString("ip_address","");
        if(IP.equals(""))
        {
            askForIP();
        }
        else
        {
            initializeView();
        }
    }

    private void initializeView()
    {
        SharedPreferences prefs = getSharedPreferences("fi.oulu.smartshophelper",MODE_PRIVATE);
        IP = prefs.getString("ip_address","");
        if(IP.equals(""))
        {
            askForIP();
        }
        else
        {
            listView = (ListView) findViewById(R.id.list_view);
            emptyView = (TextView) findViewById(R.id.empty_view);

            categories = new ArrayList<>();
            arrayAdapter = new ArrayAdapter<Category>(this, android.R.layout.simple_list_item_1, categories);

            listView.setAdapter(arrayAdapter);
            listView.setEmptyView(emptyView);

            listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                @Override
                public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                    Category category = arrayAdapter.getItem(position);
                    Intent intent = new Intent(getApplicationContext(), ItemsActivity.class);
                    intent.putExtra("category", category);
                    startActivity(intent);
                }
            });

            ((ImageButton)findViewById(R.id.cart_btn)).setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Intent intent = new Intent(getApplicationContext(),CartActivity.class);
                    startActivity(intent);
                }
            });

            new CategoriesTaks().execute();
        }
    }

    private void askForIP() {

        AlertDialog.Builder alert = new AlertDialog.Builder(this);

        alert.setTitle("Please input the server IP");
        alert.setMessage("IP inside the local network. Ex. 192.168.1.68");

        // Set an EditText view to get user input
        final EditText input = new EditText(this);
        alert.setView(input);

        alert.setPositiveButton("Ok", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int whichButton) {
                String ip = input.getText().toString();
                SharedPreferences.Editor editor = getSharedPreferences("fi.oulu.smartshophelper", MODE_PRIVATE).edit();
                editor.putString("ip_address", ip);
                editor.commit();
                initializeView();
                dialog.dismiss();
                // Do something with value!
            }
        });

        alert.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int whichButton) {
                askForIP();
            }
        });
        alert.setCancelable(false);
        alert.show();

    }

    private void getCategories(ArrayList<Category> newCategories) {

        categories.clear();


        if(newCategories!=null)
        {
            categories.addAll(newCategories);
        }


        if(categories.size()==0)
        {
            emptyView.setText("No categories available");
        }

        arrayAdapter.notifyDataSetChanged();
    }

    private class CategoriesTaks extends AsyncTask<Void, Void, ArrayList<Category>>
    {

        @Override
        protected ArrayList<Category> doInBackground(Void... params) {
            String result;
            String URL = "http://"+IP+":5000/shop/api/items/";
            HttpClient client = new DefaultHttpClient();
            ArrayList<Category> resultCategories = null;
            Log.d("Task","started");
            try
            {
                StringBuilder builder = new StringBuilder();
                HttpGet request = new HttpGet(URL);
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

                    JSONArray jsonArray = new JSONArray(result);
                    resultCategories = new ArrayList<>();

                    for(int i = 0; i<jsonArray.length(); i++)
                    {
                        JSONObject jsonCategory = jsonArray.getJSONObject(i);

                        String name = jsonCategory.getString("category");

                        JSONArray jsonArrayItems = jsonCategory.getJSONArray("items");
                        ArrayList<Item> categoriesItems = new ArrayList<>();
                        for(int j = 0; j<jsonArrayItems.length(); j++)
                        {
                            JSONObject jsonItem = jsonArrayItems.getJSONObject(j);
                            String item_name = jsonItem.getString("name");
                            String item_uri = jsonItem.getString("item_uri");

                            categoriesItems.add(new Item(item_uri,item_name));
                        }
                        resultCategories.add(new Category(name,categoriesItems));

                    }

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
            return resultCategories;
        }

        @Override
        protected void onPostExecute(ArrayList<Category> newCategories) {
            getCategories(newCategories);
        }
    }
}
