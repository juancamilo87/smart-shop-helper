package fi.oulu.smartshophelper.ui;

import android.view.LayoutInflater;
import android.view.View;
import android.widget.TextView;

import fi.oulu.smartshophelper.R;
import fi.oulu.smartshophelper.model.Store;

/**
 * Created by researcher on 01/07/15.
 */
public class Header implements ResultItem {
    private final Store store;

    public Header(Store store) {
        this.store = store;
    }

    @Override
    public int getViewType() {
        return SearchResultAdapter.RowType.HEADER_ITEM.ordinal();
    }

    @Override
    public View getView(LayoutInflater inflater, View convertView) {
        View view;
        if (convertView == null) {
            view = (View) inflater.inflate(R.layout.header_row, null);
            // Do some initialization
        } else {
            view = convertView;
        }

        TextView text = (TextView) view.findViewById(R.id.tv_store);
        text.setText(store.getName());

        return view;
    }

    public Store getStore() {
        return store;
    }
}