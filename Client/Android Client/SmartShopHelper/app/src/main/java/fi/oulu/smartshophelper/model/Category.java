package fi.oulu.smartshophelper.model;

import java.io.Serializable;
import java.util.ArrayList;

/**
 * Created by researcher on 30/06/15.
 */
public class Category implements Serializable{

    private String name;
    private ArrayList<Item> items;

    public Category(String name, ArrayList<Item> items) {
        this.name = name;
        this.items = items;
    }

    public String getName() {
        return name;
    }

    public ArrayList<Item> getItems() {
        return items;
    }

    @Override
    public String toString() {
        return name;
    }
}
