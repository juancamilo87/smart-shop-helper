package fi.oulu.smartshophelper.ui;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ListView;

import java.util.ArrayList;
import java.util.List;

import fi.oulu.smartshophelper.R;
import fi.oulu.smartshophelper.db.CartDataSource;
import fi.oulu.smartshophelper.model.CartItem;

/**
 * Created by researcher on 01/07/15.
 */
public class CartActivity extends Activity {

    private ListView listView;
    private Button searchBtn;
    private List<CartItem> items;
    private CartAdapter cartAdapter;
    private EditText edt_distance;

    private String IP;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_cart);

        SharedPreferences prefs = getSharedPreferences("fi.oulu.smartshophelper",MODE_PRIVATE);
        IP = prefs.getString("ip_address","");

        items = new ArrayList<>();

        listView = (ListView) findViewById(R.id.list_view);
        edt_distance = (EditText) findViewById(R.id.edt_distance);
        searchBtn = (Button) findViewById(R.id.search_btn);

        cartAdapter = new CartAdapter(this, R.layout.cart_row, items);

        listView.setAdapter(cartAdapter);
        listView.setEmptyView(findViewById(R.id.empty_view));

        getItems();

        searchBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int distance = 3;
                try {
                    distance = Integer.parseInt(edt_distance.getText().toString());
                } catch (Exception e) {
                }
                Intent intent = new Intent(getApplicationContext(), SearchResultActivity.class);
                intent.putExtra("distance", distance);
                startActivity(intent);
            }
        });

        ((ImageButton)findViewById(R.id.back_btn)).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

    }

    private void getItems() {
        items.clear();
        CartDataSource cartDataSource = new CartDataSource(this);
        cartDataSource.open();
        items.addAll(cartDataSource.getAllItems());
        cartDataSource.close();

        cartAdapter.notifyDataSetChanged();
    }
}
