var start = 0;

function like(id1, id2) {
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:5000/like',
        data: {'id1': id1, 'id2': id2},
        success: function (response) {
            alert(response);
        },
        error: function (error) {
            alert(error);
        }
    });
    match(id1, id2);
    showallusers(id1);
}

function match(id1, id2) {
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:5000/match',
        data: {'id1': id1, 'id2': id2},
        success: function (response) {
            alert(response);
        },
        error: function (error) {
            alert(error);
        }
    });
}

function unlike(id1, id2) {
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:5000/unlike',
        data: {'id1': id1, 'id2': id2},
        success: function (response) {
            alert(response);
        },
        error: function (error) {
            alert(error);
        }
    });
    showallusers(id1);
}

function likeButton(id1, id2) {
    function Like() {
        like(id1, id2);
    }

    var $input = $('<input type="button" value="like" />');
    $input.appendTo($(".show"));
    $input.click(function () {
        Like();
    });

}

function unlikeButton(id1, id2) {
    function Unike() {
        unlike(id1, id2);
    }

    var $input = $('<input type="button" value="unlike" />');
    $input.appendTo($(".show"));
    $input.click(function () {
        Unike();
    });

}

function showallusers(id) {
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:5000/viewallusers',
        success: function (response) {
            users = response['users'];
            $('.box').empty();
            $('.show').empty();
            likeButton(id, users[start]['id']);
            $('.box').append(users[start]['name']);
            $('#theDiv').empty();
            // $('.image').html('<img src="../static/images/user_images' + users[start]['id'] + '.jpg"
            // width = "200px" > ');
            var img=document.createElement("img");
                img.src = "/static/images/user_images/" + users[start]['id'] + ".jpg";
                img.style = "height: 400px ; width: 280px";
				document.getElementById('theDiv').appendChild(img);
            $('#theDiv').append("<h1>abc</h1>");
            unlikeButton(id, users[start]['id']);
            console.log(users[start]['name']);
            $('.show').append("<br/><br/>");
            start++;
        },
        error: function (error) {
            alert(error);
        }
    });

}