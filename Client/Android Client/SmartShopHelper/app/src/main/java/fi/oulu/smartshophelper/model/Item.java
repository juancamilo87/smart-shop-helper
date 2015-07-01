package fi.oulu.smartshophelper.model;

import java.io.Serializable;
import java.util.ArrayList;

/**
 * Created by researcher on 30/06/15.
 */
public class Item implements Serializable {

    private String name;
    private String price_uri;
    private String description;
    private String id;
    private String item_uri;
    private boolean full;
    private ArrayList<Price> prices;

    public Item(String name, String price_uri, String description, String id) {
        this.name = name;
        this.price_uri = price_uri;
        this.description = description;
        this.id = id;
        full = true;
    }

    public Item(String item_uri, String name) {
        this.item_uri = item_uri;
        this.name = name;
        full = false;
    }

    public String getName() {
        return name;
    }

    public String getPrice_uri() {
        return price_uri;
    }

    public String getDescription() {
        return description;
    }

    public String getId() {
        return id;
    }

    public String getItem_uri() {
        return item_uri;
    }

    public boolean isFull() {
        return full;
    }

    public void fill(String price_uri, String description, String id) {
        this.price_uri = price_uri;
        this.description = description;
        this.id = id;
        full = true;
    }

    public ArrayList<Price> getPrices() {
        return prices;
    }

    public void setPrices(ArrayList<Price> prices) {
        this.prices = prices;
    }

    @Override
    public String toString() {
        return name;
    }
}
