package fi.oulu.smartshophelper.model;

import android.widget.ProgressBar;

import java.io.Serializable;
import java.util.ArrayList;

/**
 * Created by researcher on 30/06/15.
 */
public class Store implements Serializable {

    private String name;
    private String address;
    private double latitude;
    private double longitude;
    private String store_id;

    private String store_uri;
    private double distance;

    private boolean full;

    private ArrayList<Price> items;

    private double totalPrice;

    public Store(String name, String address, double latitude, double longitude, String store_id) {
        this.name = name;
        this.address = address;
        this.latitude = latitude;
        this.longitude = longitude;
        this.store_id = store_id;
        full = true;
        items = new ArrayList<>();
    }

    public Store(String store_uri, double distance) {
        this.store_uri = store_uri;
        this.distance = distance;
        full = false;
        items = new ArrayList<>();
    }

    public String getName() {
        return name;
    }

    public String getAddress() {
        return address;
    }

    public double getLatitude() {
        return latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public String getStore_id() {
        return store_id;
    }

    public void fill(String name, String address, double latitude, double longitude, String store_id) {
        this.name = name;
        this.address = address;
        this.latitude = latitude;
        this.longitude = longitude;
        this.store_id = store_id;
        full = true;
    }

    public String getStore_uri() {
        return store_uri;
    }

    public double getDistance() {
        return distance;
    }

    public boolean isFull() {
        return full;
    }

    @Override
    public String toString() {
        return name;
    }

    public void refreshTotal()
    {
        totalPrice = 0;
        for(int i = 0; i<items.size();i++)
        {
            totalPrice +=(items.get(i).getPrice()*items.get(i).getQuantity());
        }
    }

    public void addItem(Price item)
    {
        items.add(item);
        refreshTotal();
    }

    public void deleteItem(Price item)
    {
        items.remove(item);
    }

    public ArrayList<Price> getItems()
    {
        return items;
    }

    public double getTotalPrice() {
        return totalPrice;
    }
}
