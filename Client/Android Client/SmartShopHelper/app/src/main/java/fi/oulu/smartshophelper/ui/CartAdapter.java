package fi.oulu.smartshophelper.ui;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.util.List;

import fi.oulu.smartshophelper.R;
import fi.oulu.smartshophelper.model.CartItem;

/**
 * Created by researcher on 01/07/15.
 */
public class CartAdapter extends ArrayAdapter {
    private final Context context;
    private final List<CartItem> items;

    public CartAdapter(Context context,int resourceId, List<CartItem> items) {
        super(context, resourceId, items);
        this.context = context;
        this.items = items;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        View rowView = convertView;
        ViewHolder view;

        if(rowView == null)
        {
            // Get a new instance of the row layout view
            LayoutInflater inflater = (LayoutInflater) getContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            rowView = inflater.inflate(R.layout.cart_row, null);

            // Hold the view objects in an object, that way the don't need to be "re-  finded"
            view = new ViewHolder();
            view.item_name = (TextView) rowView.findViewById(R.id.cart_name);
            view.item_quantity = (TextView) rowView.findViewById(R.id.cart_quantity);

            rowView.setTag(view);
        } else {
            view = (ViewHolder) rowView.getTag();
        }

        /** Set data to your Views. */
        CartItem item = items.get(position);
        view.item_name.setText(item.getName());
        view.item_quantity.setText(item.getQuantity()+"");

        return rowView;
    }

    protected static class ViewHolder{
        protected TextView item_name;
        protected TextView item_quantity;
    }
}