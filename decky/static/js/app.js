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
          if (!deck.cards[card_return.card_id]) {
            var newRow = $('<tr class="row-' + card_return.card_id + '"><td class="text-right quantity">' + cardQuantity + '</td><td><a href="/card/' + card_return.card_id + '" target="_blank" class="tooltip" data-img="' + card_return.card_id + '">' + cardName + '</a></td><td>' + card_return.card_set + '</td><td>' + card_return.card_type + '</td><td><input type="checkbox" id="' + card_return.card_id + '"><label for="' + card_return.card_id + '"></label></td><td><input type="radio" name="featured" id="' + card_return.card_id + 'f"><label for="' + card_return.card_id + 'f"></label></td><td><input type="radio" name="commander" id="' + card_return.card_id + 'c"><label for="' + card_return.card_id + 'c"></label></td><td class="text-center"><a href="" class="delete-card"><svg class="cancel" xmlns="http://www.w3.org/2000/svg"x="0px" y="0px" viewBox="0 0 823.93427 1029.8962375"><title>Cancel</title><path d="m 776.75678,0 c -12.064,0 -24.124,4.608 -33.345,13.828 L 411.94378,345.27301 80.52575,13.879 c -18.443,-18.441 -48.255,-18.441 -66.695,0 -18.441,18.44 -18.441,48.244 0,66.685 l 331.418,331.39601 -331.418,331.399 c -18.441,18.44 -18.441,48.25 0,66.691 9.198,9.198 21.272,13.817 33.347,13.817 12.073,0 24.15,-4.619 33.348,-13.817 l 331.41803,-331.398 331.468,331.445 c 9.197,9.198 21.271,13.82 33.345,13.82 12.074,0 24.101,-4.622 33.346,-13.82 18.442,-18.441 18.442,-48.247 0,-66.687 l -331.464,-331.446 331.464,-331.44501 c 18.442,-18.441 18.442,-48.25 0,-66.691 C 800.88178,4.608 788.81678,0 776.75678,0 Z"/></svg></a></td></tr>');
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
        } else {
          // If card isn't found, flash an error and select the text in the form
          flash('<strong>Oops!</strong> Looks like no card exists with that name.', 'error');
          $('.card-name').select();
        }
      }
    });
  });
  $('.builder-table tbody').on('click', '.delete-card', function(event) {
    event.preventDefault();
    var row = $(this).closest('tr');
    var rowId = row.attr('class').slice(4);
    deck.totalQuantity = deck.totalQuantity - deck.cards[rowId]['quantity']
    delete deck.cards[rowId];
    row.remove();
    // Update the quantity display on the UI
    $('.builder-quantity').text(deck.totalQuantity);
  });
  $('.save-deck').click(function() {
    event.preventDefault();
    deck.name = $('[name="name"]').val();
    deck.description = $('.description').val();
    deck.formats = $('[name="formats"]').val();
    deck.tags = $('[name="tags"]').val();
    if (deck.name == "") {
      flash('<strong>Oops!</strong> Looks like your deck doesn\’t have a name.', 'error');
    } else if (deck.formats == "") {
      flash('<strong>Oops!</strong> Looks like your deck doesn\’t have any formats.', 'error');
    } else if (deck.tags == "") {
      flash('<strong>Oops!</strong> Looks like your deck doesn\’t have any tags.', 'error');
    } else if (deck.description == "") {
      flash('<strong>Oops!</strong> Looks like your deck doesn\’t have a description.', 'error');
    } else if ( deck.cards.length == undefined ) {
      flash('<strong>Oops!</strong> Looks like your deck doesn\’t have any cards in it.', 'error');
    } else {
      var cardRequest = $.ajax({
        type: 'POST',
        url: '/add_deck',
        data: JSON.stringify(deck),
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        success: function(deck_return) {
          console.log('success')
        }
      });
      flash('<strong>Double, double toil and trouble!</strong> ' + deck.name + ' was brewed successfully.', 'success')
    }
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
    console.log('hover');
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
