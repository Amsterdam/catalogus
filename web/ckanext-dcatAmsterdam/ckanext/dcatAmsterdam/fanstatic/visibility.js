$(document).ready(function () {
initialize();
});

initialize = function() {
  $('#field-dataclassificatie').on('change', visibility_onChange);
  visibility_onChange(); //Initial
};

visibility_onChange = function() {
  var ds_dataclassificatie = $('#field-dataclassificatie').val();

  if (ds_dataclassificatie == 'Open') {
    $('#field-private').val('False');            //Set privacy
  } else {
    $('#field-private').val('True');           //Set privacy
  }
};
