package fi.oulu.smartshophelper.db;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

/**
 * Created by JuanCamilo on 5/7/2015.
 */
public class MySQLiteHelper extends SQLiteOpenHelper {

    private static final String DATABASE_NAME = "cart.db";
    private static final int DATABASE_VERSION = 4;

    public static final String TABLE_CART = "cart";
    public static final String COLUMN_CART_ID = "_id";
    public static final String COLUMN_CART_ITEM_ID = "item_id";
    public static final String COLUMN_CART_ITEM_QUANTITY = "quantity";
    public static final String COLUMN_CART_PRICE_URI = "price_uri";
    public static final String COLUMN_CART_ITEM_NAME = "name";
    public static final String COLUMN_CART_ITEM_DESCRIPTION = "description";

    private static final String CREATE_TABLE_CART = "create table "
            + TABLE_CART + "(" +
            COLUMN_CART_ID + " integer primary key autoincrement, " +
            COLUMN_CART_ITEM_ID + " text not null, " +
            COLUMN_CART_ITEM_QUANTITY + " number not null, " +
            COLUMN_CART_PRICE_URI + " text not null, " +
            COLUMN_CART_ITEM_NAME + " text not null, " +
            COLUMN_CART_ITEM_DESCRIPTION + " text, " +
            "UNIQUE ("+COLUMN_CART_ITEM_ID+") ON CONFLICT REPLACE);";

    
    public MySQLiteHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase sqLiteDatabase) {
        sqLiteDatabase.execSQL(CREATE_TABLE_CART);
    }

    @Override
    public void onUpgrade(SQLiteDatabase sqLiteDatabase, int i, int i2) {
        // on upgrade drop older tables
        sqLiteDatabase.execSQL("DROP TABLE IF EXISTS " + TABLE_CART);

        // create new tables
        onCreate(sqLiteDatabase);
    }
}
