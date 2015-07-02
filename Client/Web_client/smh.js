
ENTRY = "http://10.20.214.109:5000/shop/api/items/"

function getItems(){
	//TODO 3: Send the AJAX to retrieve the history information. Do not implement the handlers yet, just show some DEBUG text in the console. 
	//TODO 4: Implement the handlers successful and failures responses accordding to the function documentation.
	return $.ajax({
		url: "http://localhost:5000/shop/api/items/",
		type: "GET"
	}).done(function (data, textStatus, jqXHR){
		console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		showItems(data)
		/* console.log (data.collection.items.length)
		$('#messagesNumber').text(data.collection.items.length)
		$.each(data.collection.items, function(){
		
			getMessage(this.href)
		}) */	




	}).fail(function (jqXHR, textStatus, errorThrown){
		console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		$(alert('The target user history could not be retrieved'))
		//deselectUser()

	});
}

function showItems(data){
	var jsondata=$.parseJSON(data);
    $.each(jsondata, function(i, it) {
    	$.each(it.items, function(i, ite) {
    
        $('<tr>').append(
            $('<td>').text(it.category),
            $('<td>').text(ite.name),
            '<input name="DelItems" type="button" value="Delete items" onclick="deleteItem('+"'"+ite.item_uri+"'"+')" />'
        ).appendTo('#item_table');
        // $('#records_table').append($tr);
        //console.log($tr.wrap('<p>').html());
    });

       });
}

$(function() {
    
});

function deleteItem(item_uri){
	//console.log(item_uri);
	return $.ajax({
		url: "http://localhost:5000"+item_uri,
		type: "DELETE"
	}).done(function (data, textStatus, jqXHR){
		console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		/* console.log (data.collection.items.length)
		$('#messagesNumber').text(data.collection.items.length)
		$.each(data.collection.items, function(){
		
			getMessage(this.href)
		}) */	




	}).fail(function (jqXHR, textStatus, errorThrown){
		console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		$(alert('The target user history could not be retrieved'))
		//deselectUser()

	});

}



function getStores(){
	
	return $.ajax({
		url: "http://10.20.214.109:5000/shop/api/stores/",
		type: "GET"
	}).done(function (data, textStatus, jqXHR){
		console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		/* console.log (data.collection.items.length)
		$('#messagesNumber').text(data.collection.items.length)
		$.each(data.collection.items, function(){
		
			getMessage(this.href)
		}) */	




	}).fail(function (jqXHR, textStatus, errorThrown){
		console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		$(alert('The target user history could not be retrieved'))
		//deselectUser()

	});
}