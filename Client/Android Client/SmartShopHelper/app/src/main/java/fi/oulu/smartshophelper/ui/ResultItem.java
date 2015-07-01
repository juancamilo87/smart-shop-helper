package fi.oulu.smartshophelper.ui;

import android.view.LayoutInflater;
import android.view.View;

/**
 * Created by researcher on 01/07/15.
 */
public interface ResultItem {
    public int getViewType();
    public View getView(LayoutInflater inflater, View convertView);
}
