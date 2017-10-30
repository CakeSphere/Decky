$(function () {
  // Add rows to the Builder table when the user clicks Add.
  $('.add-row').click(function() {
    event.preventDefault();
    var cardQuantity = $('.card-quantity').val();
    var cardName = $('.card-name').val();
    var data = { cardName: cardName };
    var deck = [];
    var cardRequest = $.ajax({
      type: 'POST',
      url: window.location.href,
      data: JSON.stringify(data),
      dataType: 'json',
      contentType: 'application/json; charset=utf-8',
      success: function(card_return) {
        if (card_return.card_found != false) {
          if (cardName.length >= 3 && cardQuantity.length) {
            var newRow = $('<tr><td class="text-right">' + cardQuantity + '</td><td><a href="/card/' + card_return.card_id + '">' + cardName + '</a></td><td>' + card_return.card_set + '</td><td>' + card_return.card_type + '</td><td><input type="checkbox" id="' + card_return.card_id + '"><label for="' + card_return.card_id + '"></label></td><td><input type="radio" name="featured" id="' + card_return.card_id + 'f"><label for="' + card_return.card_id + 'f"></label></td><td><input type="radio" name="commander" id="' + card_return.card_id + 'c"><label for="' + card_return.card_id + 'c"></label></td></tr>');
            $('.builder-table tbody').append(newRow);
            //Reset the form
            $('.card-quantity').val(1);
            $('.card-name').val('').focus();
          }
          deck[card_return.card_id] = {
            "quantity": cardQuantity,
            "name": cardName
          };
        } else {
          $('.top-nav').append('<div class="error flash"><strong>Oops!</strong> Looks like no card exists with that name.</div>');
          $('.card-name').select();
        }
      }
    });
    console.log(deck);
  });
  $('.tooltip').hover(function(e) {
    // Card tooltips
    this.t = $(this).attr('data-img');
    $('body').append('<div class="card-preview"><img src="http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=' + this.t + '&type=card"/></div>');
    $('.card-preview')
      .css("top",(e.pageY - 10) + "px")
      .css("left",(e.pageX + 30) + "px");
  },
  function() {
    $('.card-preview').fadeOut(200, complete);
  });
  function complete() {
    this.remove();
  }
  $('.tooltip').mousemove(function(e){
    $('.card-preview')
      .css("top",(e.pageY - 10) + "px")
      .css("left",(e.pageX + 30) + "px");
  });
  $('.account-info').click(function() {
    // Show and hide the sign in dialog
    if (!$(this).hasClass('open')) {
      $(this).addClass('open');
      $('.email').focus();
    }
  });
  $(document).click(function(event) {
    if(!$(event.target).closest('.account-info').length) {
      if($('.account-info').hasClass('open')) {
        $('.account-info').removeClass('open');
      }
    }
  });
});
