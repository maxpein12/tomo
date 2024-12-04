document.querySelectorAll('.get-started').forEach(button => {
    button.addEventListener('click', function() {
        alert("You clicked the Get Started button!");
    });
});


$(document).ready(function() {
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
    
    // Store the old value of the input field when the page loads
    $('td:not(:last-child)').each(function() {
        var cell = $(this);
        var input = cell.find('input');
        if (input.length > 0) {
            cell.data('old-value', input.val());
        } else {
            cell.data('old-value', cell.text());
        }
    });
    
    $(document).on('click', '.edit-btn', function() {
        var row = $(this).closest('tr');
        var id = row.data('id');
        
        row.find('td:not(:last-child)').each(function() {
            var cell = $(this);
            var text = cell.text();
            cell.html('<input type="text" value="' + text + '">');
        });
        
        $(this).text('Save').removeClass('edit-btn').addClass('save-btn');
    });
    
    $(document).on('click', '.save-btn', function() {
        var row = $(this).closest('tr');
        var id = row.data('id');
        var data = {
            'id': id
        };
        
        row.find('td:not(:last-child)').each(function() {
            var cell = $(this);
            var input = cell.find('input');
            if (input.length > 0) {
                var newValue = input.val();
                var oldValue = cell.data('old-value');
                if (oldValue !== newValue) {
                    if (cell.index() === 0) {
                        data['pkpoint_bundle'] = newValue;
                    } else if (cell.index() === 1) {
                        data['price'] = newValue;
                    } else if (cell.index() === 2) {
                        data['name'] = newValue;
                    } else if (cell.index() === 3) {
                        data['description'] = newValue;
                    }
                }
            }
        });
        
        // Send a default value for pkpoint_bundle if it's not being updated
        if (!('pkpoint_bundle' in data)) {
            var pkpoint_bundle = row.find('td:eq(0)').text();
            if (pkpoint_bundle !== '') {
                data['pkpoint_bundle'] = pkpoint_bundle;
            }
        }
        
        
        
        $.ajax({
            type: 'POST',
            url: updatePriceUrl,
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function(response) {
                if (response.status == 'success') {
                    alert('Data updated successfully!');
                    location.reload();
                } else {
                    alert('Error updating data!');
                }
            }
        });
        
        $(this).text('Edit').removeClass('save-btn').addClass('edit-btn');
        
        row.find('td:not(:last-child)').each(function() {
            var cell = $(this);
            var input = cell.find('input');
            cell.data('old-value', input.val());
            cell.html(input.val());
        });
    });
});


// 1	20000.00	150通	            150分	                編集
// 2	14000.00	90通	            90分	                編集
// 3	10000.00	60通	            60分	                編集
// 4	5800.00	    30通　	            30分	                編集
// 5	2000.00	    10通	            10分	                編集
// 6	1000.00	    5通	                5分                     編集
// 7	0.00	    無料通話ポイント	   初回限定無料 10分        編集
// 8	0.00	    無料メッセージポイント	初回限定無料 10通	     編集