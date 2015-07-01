package fi.oulu.smartshophelper.ui;

import android.view.LayoutInflater;
import android.view.View;
import android.widget.TextView;

import fi.oulu.smartshophelper.R;

/**
 * Created by researcher on 01/07/15.
 */
public class ListItem implements ResultItem {
    private final String str1;
    private final String str2;
    private final String str3;

    public ListItem(String name, String quantity, String price) {
        this.str1 = name;
        this.str2 = quantity;
        this.str3 = price;
    }

    @Override
    public int getViewType() {
        return SearchResultAdapter.RowType.LIST_ITEM.ordinal();
    }

    @Override
    public View getView(LayoutInflater inflater, View convertView) {
        View view;
        if (convertView == null) {
            view = (View) inflater.inflate(R.layout.list_item_row, null);
            // Do some initialization
        } else {
            view = convertView;
        }

        TextView text1 = (TextView) view.findViewById(R.id.tv_item_name);
        TextView text2 = (TextView) view.findViewById(R.id.tv_quantity);
        TextView text3 = (TextView) view.findViewById(R.id.tv_price);
        text1.setText(str1);
        text2.setText(str2);
        text3.setText(str3);

        return view;
    }

}