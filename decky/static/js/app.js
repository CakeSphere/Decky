$(function () {
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
        console.log(card_return[`card_set`]);
        if (cardName.length >= 3 && cardQuantity.length >= 1) {
          var newRow = $('<tr><td class="text-right">' + cardQuantity + '</td><td><a href="/card/' + card_return['card_id'] + '">' + cardName + '</a></td><td>' + card_return['card_set'] + '</td><td>' + card_return['card_type'] + '</td><td><input type="checkbox" id="' + card_return['card_id'] + '"><label for="' + card_return['card_id'] + '"></label></td><td><input type="radio" name="featured" id="' + card_return['card_id'] + 'f"><label for="' + card_return['card_id'] + 'f"></label></td><td><input type="radio" name="commander" id="' + card_return['card_id'] + 'c"><label for="' + card_return['card_id'] + 'c"></label></td></tr>');
          $('.builder-table tbody').append(newRow);
          $('.card-quantity').val(1);
          $('.card-name').val('').focus();
        }
      }
    });
  });
  $('.account-info').click(function() {
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
