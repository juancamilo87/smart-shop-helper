package fi.oulu.smartshophelper.model;

/**
 * Created by researcher on 01/07/15.
 */
public class CartItem extends Item {

    private int quantity;

    public CartItem(String name, String price_uri, String description, String id, int quantity) {
        super(name, price_uri, description, id);
        this.quantity = quantity;
    }

    public int getQuantity() {
        return quantity;
    }
}
