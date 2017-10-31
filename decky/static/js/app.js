$(function () {
  // Instantiate the deck object for the builder
  var deck = {
    "totalQuantity": 0
  };
  // Hide all tabs on page load
  $('[class^=tab-]').hide();
  // Show the first tab by default
  $('.tab-1').show();
  // Add rows to the Builder table when the user clicks Add.
  $('.add-row').click(function() {
    event.preventDefault();

    var cardQuantity = $('.card-quantity').val();
    var cardName = $('.card-name').val();
    var data = { cardName: cardName };

    var cardRequest = $.ajax({
      type: 'POST',
      url: window.location.href,
      data: JSON.stringify(data),
      dataType: 'json',
      contentType: 'application/json; charset=utf-8',
      success: function(card_return) {
        if (card_return.card_found != false) {
          var newRow = $('<tr><td class="text-right">' + cardQuantity + '</td><td><a href="/card/' + card_return.card_id + '" class="tooltip" data-img="' + card_return.card_id + '">' + cardName + '</a></td><td>' + card_return.card_set + '</td><td>' + card_return.card_type + '</td><td><input type="checkbox" id="' + card_return.card_id + '"><label for="' + card_return.card_id + '"></label></td><td><input type="radio" name="featured" id="' + card_return.card_id + 'f"><label for="' + card_return.card_id + 'f"></label></td><td><input type="radio" name="commander" id="' + card_return.card_id + 'c"><label for="' + card_return.card_id + 'c"></label></td></tr>');
          // Add a new row to the builder table
          $('.builder-table tbody').append(newRow);
          // Reset the form
          $('.card-quantity').val(1);
          $('.card-name').val('').focus();
          // Add the card to the deck object
          deck[card_return.card_id] = {
            "quantity": cardQuantity,
            "foil": false,
            "featured": false,
            "commander": false
          };
          // Update the total quantity with the number of cards added
          deck.totalQuantity = deck.totalQuantity + Number(cardQuantity);
          // Update the quantity display on the UI
          $('.builder-quantity').text(deck.totalQuantity);
          console.log(deck);
        } else {
          // If card isn't found, flash an error and select the text in the form
          $('.top-nav').append('<div class="error flash"><strong>Oops!</strong> Looks like no card exists with that name.</div>');
          $('.card-name').select();
        }
      }
    });
  });
  $('.tabs .btn').click(function() {
    // Handle hiding and showing tabs
    event.preventDefault();
    var tab = $(this).attr('data-tab');
    $('.tabs .btn').removeClass('active');
    $('[class^="tab-"]').hide();
    $(this).addClass('active');
    $('.' + tab).show();
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
    // Hide the tooltip when user mouses out
    $('.card-preview').fadeOut(100, complete);
  });
  function complete() {
    // Delete the tooltip when it finishes fading out
    this.remove();
  }
  $('.tooltip').mousemove(function(e){
    // Move the tooltip when the mouse moves
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
    // Close the sign in dialog when the user clicks outside it
    if(!$(event.target).closest('.account-info').length) {
      if($('.account-info').hasClass('open')) {
        $('.account-info').removeClass('open');
      }
    }
  });
});
