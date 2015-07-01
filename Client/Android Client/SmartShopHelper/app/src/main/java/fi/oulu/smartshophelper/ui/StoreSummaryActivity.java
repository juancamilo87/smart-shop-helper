package fi.oulu.smartshophelper.ui;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextView;

import fi.oulu.smartshophelper.R;
import fi.oulu.smartshophelper.model.Store;

/**
 * Created by researcher on 02/07/15.
 */
public class StoreSummaryActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_store_summary);

        Store store = (Store) getIntent().getSerializableExtra("store");

        ((TextView)findViewById(R.id.store_name)).setText(store.getName());
        ((TextView)findViewById(R.id.store_address)).setText(store.getAddress());

        ((ImageButton)findViewById(R.id.back_btn)).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
    }
}
