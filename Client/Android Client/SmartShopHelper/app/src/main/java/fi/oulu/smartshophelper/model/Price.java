package fi.oulu.smartshophelper.model;

import java.io.Serializable;

/**
 * Created by researcher on 30/06/15.
 */
public class Price implements Serializable {

    private double price;
    private long timestamp;
    private String store_uri;
    private Store store;
    private String item_id;
    private String name;
    private int quantity;

    public Price(double price, long timestamp, String store_uri, String item_id, String name, int quantity) {
        this.price = price;
        this.timestamp = timestamp;
        this.store_uri = store_uri;
        this.item_id = item_id;
        this.name = name;
        this.quantity = quantity;
    }

    public double getPrice() {
        return price;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public String getStore_uri() {
        return store_uri;
    }

    public Store getStore() {
        return store;
    }

    public void setStore(Store store) {
        this.store = store;
    }

    public String getItem_id() {
        return item_id;
    }

    public String getName() {
        return name;
    }

    public int getQuantity() {
        return quantity;
    }
}
