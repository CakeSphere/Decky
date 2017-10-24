$(function () {
  $('.add-row').click(function() {
    event.preventDefault();
    var cardQuantity = $('.card-quantity').val();
    var cardName = $('.card-name').val();
    var newRow = $('<tr><td class="text-right">' + cardQuantity + '</td><td><a href="/card">' + cardName + '</a></td><td>Kaladesh</td><td>Land</td><td><input type="checkbox" id="1"><label for="1"></label></td><td><input type="radio" name="featured" id="1f"><label for="1f"></label></td><td><input type="radio" name="commander" id="1c"><label for="1c"></label></td></tr>');
    $('.builder-table tbody').append(newRow);
    var data = {
      cardName: cardName
    };
    $.ajax({
      type: 'POST',
      url: window.location.href,
      data: JSON.stringify(data),
      dataType: 'json',
      contentType: 'application/json; charset=utf-8'
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
