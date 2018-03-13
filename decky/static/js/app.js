$(function () {
  // Instantiate the deck object for the builder
  var deck;
  if (typeof edit_deck != 'undefined') {
    var editMode = true;
    deck = edit_deck;
    console.log(deck)
    $('.builder-quantity').text(deck.totalQuantity);
    $('.builder-table').show();
  } else {
    deck = {
      'totalQuantity': 0,
      cards: {},
      'edit_id': '',
      makeup: []
    };
  }
  // Show the first tab by default
  $('.tab-1').show();
  // Delete Deck
  $('.delete').click(function(event) {
    event.preventDefault();
    $('.dialog').show();
    $('.dialog-bg').fadeIn(100);
  });
  function compareNumbers(a, b) {
    return a - b;
  }
  // Close dialog
  $('.close').click(function(event) {
    event.preventDefault();
    $('.dialog').fadeOut(100);
    $('.dialog-bg').fadeOut(100);
  });
  // Add rows to the Builder table when the user clicks Add.
  $('.add-row').click(function(event) {
    event.preventDefault();
    $('.builder-table').show();
    var cardQuantity = parseInt($('.card-quantity').val());
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
            var sets = Object.getOwnPropertyNames(card_return.card_sets).sort(compareNumbers).reverse();
            var newRow = $('<tr class="row-' + card_return.card_id + '"><td class="text-right quantity">' + cardQuantity + '</td><td><a href="/card/' + card_return.card_id + '" target="_blank" class="tooltip" data-img="' + card_return.card_id + '">' + cardName + '</a></td><td><select class="btn" id="select-set-' + card_return.card_id + '"></select></td><td>' + card_return.card_type + '</td><td><input type="checkbox" id="' + card_return.card_id + '"><label for="' + card_return.card_id + '"></label></td><td><input type="radio" name="featured" id="' + card_return.card_id + 'f"><label for="' + card_return.card_id + 'f"></label></td><td><input type="radio" name="commander" id="' + card_return.card_id + 'c"><label for="' + card_return.card_id + 'c"></label></td><td class="text-center"><a href="" class="delete-card"><svg class="cancel" xmlns="http://www.w3.org/2000/svg"x="0px" y="0px" viewBox="0 0 823.93427 1029.8962375"><title>Cancel</title><path d="m 776.75678,0 c -12.064,0 -24.124,4.608 -33.345,13.828 L 411.94378,345.27301 80.52575,13.879 c -18.443,-18.441 -48.255,-18.441 -66.695,0 -18.441,18.44 -18.441,48.244 0,66.685 l 331.418,331.39601 -331.418,331.399 c -18.441,18.44 -18.441,48.25 0,66.691 9.198,9.198 21.272,13.817 33.347,13.817 12.073,0 24.15,-4.619 33.348,-13.817 l 331.41803,-331.398 331.468,331.445 c 9.197,9.198 21.271,13.82 33.345,13.82 12.074,0 24.101,-4.622 33.346,-13.82 18.442,-18.441 18.442,-48.247 0,-66.687 l -331.464,-331.446 331.464,-331.44501 c 18.442,-18.441 18.442,-48.25 0,-66.691 C 800.88178,4.608 788.81678,0 776.75678,0 Z"/></svg></a></td></tr>');
            // Add a new row to the builder table
            $('.builder-table tbody').append(newRow);
            if (newRow.is(':first-child')) {
              newRow.find('[type=radio]').prop('checked', true);
            }
            var selectSet = document.getElementById('select-set-' + card_return.card_id);
            if (sets.length > 1) {
              for (var i = 0; i < sets.length; i++) {
                var opt = document.createElement('option');
                opt.innerHTML = card_return.card_sets[sets[i]];
                opt.value = sets[i];
                selectSet.appendChild(opt);
              }
            } else {
              selectSet.replaceWith(card_return.card_sets[sets[0]])
            }

            // Reset the form
            $('.card-quantity').val(1);
            $('.card-name').val('').focus();
            cardId = card_return.card_id;
            // Add the card to the deck object
            deck.cards[cardId] = {
              "quantity": cardQuantity,
              "foil": false,
              "featured": false,
              "commander": false,
              "makeup": card_return.card_makeup.split(', ')
            };
            // Change everything in the row and in the deck object when the
            // user changes the printing.
            $(selectSet).on('change', function () {
              // Get the parent row of the select element
              var row = $(this).parents('[class^="row"]')
              row.attr('class', 'row-' + selectSet.value);
              // Change the link to point to the new printing
              var card_link = row.find($('.tooltip'))
              var cardQuantity = Number(row.find($('.quantity')).text());
              card_link.attr('href', "/card/" + selectSet.value);
              card_link.attr('data-img', selectSet.value);
              // Get the associated inputs
              var featured = $(row).find($('input:radio[id*="f"]'));
              var commander = $(row).find($('input:radio[id*="c"]'));
              var foil = $(row).find($('input:checkbox'));
              // Delete the old printing from the deck object
              delete deck.cards[cardId];
              // Delete any previously added printings
              for (var i = 0; i < sets.length; i++) {
                delete deck.cards[sets[i]];
              }
              // Change all of the inputs and their labels to match the new
              // printing
              $(row).find($('input:radio[id*="f"] + label')).attr('for', selectSet.value + "f");
              featured.attr('id', selectSet.value + "f");
              $(row).find($('input:radio[id*="c"] + label')).attr('for', selectSet.value + "c");
              commander.attr('id', selectSet.value + "c");
              $(row).find($('input:checkbox + label')).attr('for', selectSet.value);
              foil.attr('id', selectSet.value);
              // Add the new printing to the deck object
              deck.cards[selectSet.value] = {
                "quantity": cardQuantity,
                "foil": false,
                "featured": false,
                "commander": false
              };
            });
          } else {
            // Add the quantity in the form to the quantity in the table
            var currentQuantity = Number($('.row-' + card_return.card_id + ' .quantity').text());
            currentQuantity = currentQuantity + Number(cardQuantity);
            $('.row-' + card_return.card_id + ' .quantity').text(currentQuantity);
            deck.cards[card_return.card_id].quantity = Number(deck.cards[card_return.card_id].quantity) + 1;
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
  // Change everything in the row and in the deck object when the
  // user changes the printing.
  $('[id^=select-set-]').on('focus', function () {
    cardId = this.value;
    sets = [];
    $(this).find('option').each(function() {
      sets.push(this.value);
    });
  }).change(function() {
    // Get the parent row of the select element
    var row = $(this).parents('[class^="row"]');
    row.attr('class', 'row-' + this.value);
    // Change the link to point to the new printing
    var card_link = row.find($('.tooltip'));
    var cardQuantity = Number(row.find($('.quantity')).text());
    card_link.attr('href', "/card/" + this.value);
    card_link.attr('data-img', this.value);
    // Get the associated inputs
    var featured = $(row).find($('input:radio[id*="f"]'));
    var commander = $(row).find($('input:radio[id*="c"]'));
    var foil = $(row).find($('input:checkbox'));
    // Delete the old printing from the deck object
    delete deck.cards[cardId];
    // Delete any previously added printings
    for (var i = 0; i < sets.length; i++) {
      delete deck.cards[sets[i]];
    }
    // Change all of the inputs and their labels to match the new
    // printing
    $(row).find($('input:radio[id*="f"] + label')).attr('for', this.value + "f");
    featured.attr('id', this.value + "f");
    $(row).find($('input:radio[id*="c"] + label')).attr('for', this.value + "c");
    commander.attr('id', this.value + "c");
    $(row).find($('input:checkbox + label')).attr('for', this.value);
    foil.attr('id', this.value);
    // Add the new printing to the deck object
    deck.cards[this.value] = {
      "quantity": cardQuantity,
      "foil": false,
      "featured": false,
      "commander": false
    };
  });
  $('.builder-table tbody').on('click', '.delete-card', function(event) {
    event.preventDefault();
    var row = $(this).closest('tr');
    var rowId = row.attr('class').slice(4);
    deck.totalQuantity = deck.totalQuantity - deck.cards[rowId].quantity;
    delete deck.cards[rowId];
    row.remove();
    // Update the quantity display on the UI
    $('.builder-quantity').text(deck.totalQuantity);
  });
  $('.save-deck').click(function(event) {
    event.preventDefault();
    $('.save-deck').html('<div class="btn-loader">&nbsp;</div>').width(88.15).addClass('c').disable;
    deck.name = $('[name="name"]').val();
    deck.description = $('.description').val();
    deck.formats = $('[name="formats"]').val();
    deck.tags = $('[name="tags"]').val();

    for (var card in deck["cards"]) {
      if (deck["cards"][card]["makeup"] != "") {
        deck["makeup"].push.apply(deck["makeup"], deck["cards"][card]["makeup"])
      }
    }
    // Flag cards with foil in the deck object
    var foils = $('input:checkbox:checked');
    foils.each(function(index) {
      var foilId = $(this).attr('id');
      deck.cards[foilId].foil = true;
    });

    // Flag the featured card and the commander in the deck object.
    var featured = $('input:radio:checked[id*="f"]').attr('id').slice(0,-1);
    deck.cards[featured].featured = true;
    var commander = $('input:radio:checked[id*="c"]').attr('id').slice(0,-1);
    deck.cards[commander].commander = true;
    // Should all of these fields be required?
    if (deck.name == "") {
      flash('<strong>Oops!</strong> Looks like your deck doesn\’t have a name.', 'error');
    } else if (deck.formats == "") {
      flash('<strong>Oops!</strong> Looks like your deck doesn\’t have any formats.', 'error');
    } else if (deck.tags == "") {
      flash('<strong>Oops!</strong> Looks like your deck doesn\’t have any tags.', 'error');
    } else if (deck.description == "") {
      flash('<strong>Oops!</strong> Looks like your deck doesn\’t have a description.', 'error');
    } else {
      var cardRequest = $.ajax({
        type: 'POST',
        url: '/add_deck',
        data: JSON.stringify(deck),
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        complete: function() {
          setTimeout(function() {$('.save-deck').html('<div class="btn-success"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0px" y="0px" viewBox="0 0 100 125" enable-background="new 0 0 100 100" xml:space="preserve"><path d="M92.806,32.338l-51.429,45c-0.019,0.017-0.042,0.028-0.061,0.044c-0.266,0.228-0.547,0.429-0.838,0.607  c-0.047,0.029-0.094,0.056-0.141,0.084c-0.296,0.17-0.6,0.315-0.914,0.434c-0.048,0.018-0.097,0.034-0.146,0.051  c-0.319,0.112-0.644,0.203-0.974,0.263c-0.037,0.007-0.075,0.01-0.112,0.016c-0.345,0.057-0.693,0.091-1.041,0.091  c-0.001,0-0.003,0-0.004,0c0,0-0.001,0-0.001,0c-0.001,0-0.001,0-0.002,0c-0.216,0-0.431-0.012-0.646-0.034  c-0.057-0.006-0.112-0.017-0.169-0.024c-0.158-0.02-0.317-0.042-0.473-0.074c-0.07-0.014-0.138-0.034-0.207-0.051  c-0.141-0.034-0.282-0.069-0.421-0.112c-0.077-0.024-0.153-0.053-0.229-0.08c-0.128-0.045-0.255-0.092-0.38-0.145  c-0.082-0.035-0.162-0.074-0.243-0.113c-0.115-0.055-0.229-0.112-0.341-0.174c-0.086-0.047-0.17-0.098-0.254-0.15  c-0.102-0.063-0.203-0.128-0.302-0.197c-0.087-0.061-0.173-0.124-0.258-0.19c-0.091-0.071-0.18-0.144-0.268-0.22  c-0.085-0.073-0.168-0.147-0.249-0.225c-0.034-0.033-0.071-0.061-0.104-0.094L6.883,51.332c-2.511-2.511-2.511-6.579,0-9.09  c2.511-2.511,6.579-2.511,9.09,0l21.461,21.461l46.902-41.039c2.674-2.345,6.73-2.069,9.072,0.603  C95.747,25.941,95.477,30,92.806,32.338z"/></svg></div>')}, 1750);
          setTimeout(function() {$('.save-deck').html('Save Changes').removeClass('c')}, 3500);
        },
        success: function(deck_return) {
        }
      });
    console.log(deck)
    }
  });
  // Function that does the same thing as the Python Flask flash function.
  function flash(message, type) {
    $('.top-nav').append('<div class="' + type + ' flash">' + message + '</div>');
    setTimeout(function() { $('.flash').remove(); }, 5500);
  }
  $('.tabs .btn').click(function(event) {
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
    if($(this).hasClass('foil')) {
      $('body').append('<div class="card-preview foil"><img src="http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=' + this.t + '&type=card"/></div>');
    } else {
      $('body').append('<div class="card-preview"><img src="http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=' + this.t + '&type=card"/></div>');
    }

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

  $('.builder-table tbody').on('mouseenter', '.tooltip', function(e) {
    // Card tooltips
    this.t = $(this).attr('data-img');
    if($(this).hasClass('foil')) {
      $('body').append('<div class="card-preview foil"><img src="http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=' + this.t + '&type=card"/></div>');
    } else {
      $('body').append('<div class="card-preview"><img src="http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=' + this.t + '&type=card"/></div>');
    }
    $('.card-preview')
      .css("top",(e.pageY - 10) + "px")
      .css("left",(e.pageX + 30) + "px");
  });
  $('.builder-table tbody').on('mouseleave', '.tooltip', function(e) {
    $('.card-preview').fadeOut(100, complete);
  });
  $('.builder-table tbody').on('mousemove', '.tooltip', function(e) {
    // Update the tooltip position when the mouse moves
    $('.card-preview')
      .css("top",(e.pageY - 10) + "px")
      .css("left",(e.pageX + 30) + "px");
  });
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
  var bulkEdit = $('.bulk-edit');
  var colorReg = new RegExp(/[0-9]+x/gm);
  function colorize() {
    var bulkEditText = bulkEdit.html();
    if (colorReg.test(bulkEditText)) {
      bulkEditText = bulkEditText.replace(colorReg, '<span class="count">$&</span class="count">')
      bulkEdit.html(bulkEditText);
    }
  }
  colorize();
});
