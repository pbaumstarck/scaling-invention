
function ZsonController($scope) {
  $scope.input = '' +
    '/**\n' +
    ' * Everything can start with a block comment.\n' +
    ' * Copyright MCMXLV\n' +
    ' */\n' +
    '\n' +
    '[\n' +
    '  // Start with some simple numbers.\n' +
    '  1,\n' +
    '  2,\n' +
    '  // Get ready for the next number ...\n' +
    '  4_294_967_296, // Whoa.\n' +
    '  // And now for some strings:\n' +
    '  "a",\n' +
    '  "b",\n' +
    '  """To be, or not to be: that is the question:\n' +
    'Whether \'tis nobler in the mind to suffer\n' +
    'The slings and arrows of outrageous fortune ...""",\n' +
    '  // And how about an object with multi-line keys *and* values?\n' +
    '  {\n' +
    '    """A\n' +
    'B\n' +
    'C""": """C\n' +
    'B\n' +
    '"And something quoted.\\""""\n' +
    '  },\n' +
    '  // And we allow a comma after the last item, which JSON\n' +
    '  // would die violently upon.\n' +
    '  5,\n' +
    ']\n';
  $scope.hasError = false;

  function computeOutput() {
    try {
      $scope.output = ZSON.stringify(ZSON.parse($scope.input), null, 2);
      $scope.hasError = false;
    } catch (e) {
      $scope.output = 'Sorry, there was an error parsing your ZSON.';
      $scope.hasError = true;
    }
  }
  $scope.output = computeOutput();
  $scope.$watch('input', computeOutput);
}
