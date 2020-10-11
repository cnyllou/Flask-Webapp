$(document).ready(function() {
  var $filterCheckboxes = $('.filter');

  $filterCheckboxes.on('change', function() {
    var selectedFilters = {};

    $filterCheckboxes.filter(':checked').each( function() {
      if (!selectedFilters.hasOwnProperty(this.name)) {
        selectedFilters[this.name] = [];
      }
      selectedFilters[this.name].push(this.value);
    });

    var $filteredResults = $('.catalog-item');

    $.each(selectedFilters, function(name, filterValues){
      $filteredResults = $filteredResults.filter(function(){
        var matched = false,
          currentFilterValues = $(this).data('category').split(' ');

          $.each(currentFilterValues, function(_, currentFilterValue){

            if ($.inArray(currentFilterValue, filterValues) != -1){
              matched = true;
              return false;
            }
          });
          return matched;
      });
    });

    $('.catalog-item').hide().addClass('shown').filter($filteredResults).show();
  });
});
