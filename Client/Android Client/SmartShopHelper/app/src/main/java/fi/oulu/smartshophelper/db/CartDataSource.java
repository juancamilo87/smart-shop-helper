package fi.oulu.smartshophelper.db;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.util.Log;

import java.util.ArrayList;
import java.util.List;

import fi.oulu.smartshophelper.model.CartItem;
import fi.oulu.smartshophelper.model.Item;

/**
 * Created by JuanCamilo on 5/7/2015.
 */
public class CartDataSource {

    private SQLiteDatabase database;
    private MySQLiteHelper dbHelper;
    private Context context;


    private String[] allColumns = {
            MySQLiteHelper.COLUMN_CART_ID,
            MySQLiteHelper.COLUMN_CART_ITEM_ID,
            MySQLiteHelper.COLUMN_CART_ITEM_QUANTITY,
            MySQLiteHelper.COLUMN_CART_PRICE_URI,
            MySQLiteHelper.COLUMN_CART_ITEM_NAME,
            MySQLiteHelper.COLUMN_CART_ITEM_DESCRIPTION
            };

    public CartDataSource(Context context) {
        this.context = context;
        dbHelper = new MySQLiteHelper(context);
    }

    public void open() throws SQLException {
        database = dbHelper.getWritableDatabase();
    }

    public void close() {
        dbHelper.close();
    }

    public CartItem addItem(Item item) {
        int quantity = 1;
        Cursor cursor = database.query(MySQLiteHelper.TABLE_CART,
                allColumns, MySQLiteHelper.COLUMN_CART_ITEM_ID + " like " + "'"+item.getId()+"'", null,
                null, null, null);

        if(cursor.moveToFirst())
        {
            quantity += cursor.getInt(cursor.getColumnIndex(MySQLiteHelper.COLUMN_CART_ITEM_QUANTITY));
        }
        cursor.close();

        ContentValues values = new ContentValues();
        values.put(MySQLiteHelper.COLUMN_CART_ITEM_ID, item.getId());
        values.put(MySQLiteHelper.COLUMN_CART_ITEM_QUANTITY, quantity);
        values.put(MySQLiteHelper.COLUMN_CART_PRICE_URI, item.getPrice_uri());
        values.put(MySQLiteHelper.COLUMN_CART_ITEM_NAME, item.getName());
        values.put(MySQLiteHelper.COLUMN_CART_ITEM_DESCRIPTION, item.getDescription());

        long insertId = database.insert(MySQLiteHelper.TABLE_CART, null,
                values);

        Log.d("id", insertId + "");
        Cursor otherCursor = database.query(MySQLiteHelper.TABLE_CART,
                allColumns, MySQLiteHelper.COLUMN_CART_ID + " = " + insertId, null,
                null, null, null);
        otherCursor.moveToFirst();
        CartItem newItem = cursorToCartItem(otherCursor);
        cursor.close();
        return newItem;

    }

    public void deleteItem(Item item) {
        String id = item.getId();
        database.delete(MySQLiteHelper.TABLE_CART, MySQLiteHelper.COLUMN_CART_ITEM_ID
                + " = " + id, null);
    }

    public List<CartItem> getAllItems() {
        List<CartItem> cartItems = new ArrayList<>();

        Cursor cursor = database.query(MySQLiteHelper.TABLE_CART,
                allColumns, null, null, null, null, null);

        cursor.moveToFirst();
        while (!cursor.isAfterLast()) {
            CartItem cartItem = cursorToCartItem(cursor);
            cartItems.add(cartItem);
            cursor.moveToNext();
        }
        // make sure to close the cursor
        cursor.close();
        return cartItems;
    }

    private CartItem cursorToCartItem(Cursor cursor) {
        CartItem item = null;
        try{
            long id = cursor.getLong(cursor.getColumnIndex(MySQLiteHelper.COLUMN_CART_ID));
            String item_id = cursor.getString(cursor.getColumnIndex(MySQLiteHelper.COLUMN_CART_ITEM_ID));
            int quantity = cursor.getInt(cursor.getColumnIndex(MySQLiteHelper.COLUMN_CART_ITEM_QUANTITY));
            String price_uri = cursor.getString(cursor.getColumnIndex(MySQLiteHelper.COLUMN_CART_PRICE_URI));
            String name = cursor.getString(cursor.getColumnIndex(MySQLiteHelper.COLUMN_CART_ITEM_NAME));
            String description = cursor.getString(cursor.getColumnIndex(MySQLiteHelper.COLUMN_CART_ITEM_DESCRIPTION));

            item = new CartItem(name,price_uri,description,item_id, quantity);
        }catch(Exception e){}

        return item;
    }


}
