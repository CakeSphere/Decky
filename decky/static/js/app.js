$(function () {
  // Instantiate the deck object for the builder
  var deck = {
    'totalQuantity': 0
  };
  deck.cards = {};
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
          if (!deck[card_return.card_id]) {
            var newRow = $('<tr class="row-' + card_return.card_id + '"><td class="text-right quantity">' + cardQuantity + '</td><td><a href="/card/' + card_return.card_id + '" target="_blank" class="tooltip" data-img="' + card_return.card_id + '">' + cardName + '</a></td><td>' + card_return.card_set + '</td><td>' + card_return.card_type + '</td><td><input type="checkbox" id="' + card_return.card_id + '"><label for="' + card_return.card_id + '"></label></td><td><input type="radio" name="featured" id="' + card_return.card_id + 'f"><label for="' + card_return.card_id + 'f"></label></td><td><input type="radio" name="commander" id="' + card_return.card_id + 'c"><label for="' + card_return.card_id + 'c"></label></td></tr>');
            // Add a new row to the builder table
            $('.builder-table tbody').append(newRow);
            // Reset the form
            $('.card-quantity').val(1);
            $('.card-name').val('').focus();
            cardId = card_return.card_id;
            // Add the card to the deck object
            deck.cards[cardId] = {
              "quantity": cardQuantity,
              "foil": false,
              "featured": false,
              "commander": false
            };
          } else {
            // Add the quantity in the form to the quantity in the table
            var currentQuantity = Number($('.row-' + card_return.card_id + ' .quantity').text());
            currentQuantity = currentQuantity + Number(cardQuantity);
            $('.row-' + card_return.card_id + ' .quantity').text(currentQuantity);
            // Reset the form
            $('.card-quantity').val(1);
            $('.card-name').val('').focus();
          }
          // Update the total quantity with the number of cards added
          deck.totalQuantity = deck.totalQuantity + Number(cardQuantity);
          // Update the quantity display on the UI
          $('.builder-quantity').text(deck.totalQuantity);
          console.log(deck)
        } else {
          // If card isn't found, flash an error and select the text in the form
          flash('<strong>Oops!</strong> Looks like no card exists with that name.', 'error');
          $('.card-name').select();
        }
      }
    });
  });
  $('.save-deck').click(function() {
    event.preventDefault();
    deck.name = $('[name="name"]').val();
    deck.description = $('.description').val();
    deck.formats = $('[name="formats"]').val();
    deck.tags = $('[name="tags"]').val();
    // flash('<strong>Double, double toil and trouble!</strong> ' + deck.name + ' was brewed successfully.', 'success')
    var cardRequest = $.ajax({
      type: 'POST',
      url: '/add_deck',
      data: JSON.stringify(deck),
      dataType: 'json',
      contentType: 'application/json; charset=utf-8',
      success: function(deck_return) {
        console.log('success?')
      }
    });
  });
  // Function that does the same thing as the Python Flask flash function.
  function flash(message, type) {
    $('.top-nav').append('<div class="' + type + ' flash">' + message + '</div>');
    setTimeout(function() { $('.flash').remove(); }, 5500);
  }
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
    // Update the tooltip position when the mouse moves
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
