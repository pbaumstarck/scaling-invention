
$(document).ready(function() {
  // Animate the text on the menu links.
  $("#blog-link").nyanBar({
    charSize: 6,
    pattern: "Bl{o|0}g*",
    bookends: null
  });
  $("#source-link").nyanBar({
    charSize: 6,
    pattern: "{S|s}{o|O}{U|u}{r|R}{C|c}{e|E}*",
    bookends: null
  });
  $("#bugs-link").nyanBar({
    charSize: 4,
    updatePeriod: 300,
    pattern: ("{B|B|B|B|B|B|B|B|B|B|B|B|B|#}" +
              "{u|u|u|u|u|u|u|u|u|u|u|u|u|*}" +
              "{g|g|g|g|g|g|g|g|g|g|g|g|g|!}" +
              "{s|s|s|s|s|s|s|s|s|s|s|s|s|@}*"),
    bookends: null
  });
  $("#docs-link").nyanBar({
    charSize: 4,
    updatePeriod: 1000,
    pattern: "{D|d}{O|0}{C|c}{S|$}*",
    bookends: null
  });
  $("#download-link").nyanBar({
    charSize: 8,
    updatePeriod: 125,
    pattern: ("{D|d|d|d|d|d|d|d}" +
              "{o|O|o|o|o|o|o|o}" +
              "{w|w|W|w|w|w|w|w}" +
              "{n|n|n|N|n|n|n|n}" +
              "{l|l|l|l|L|l|l|l}" +
              "{o|o|o|o|o|O|o|o}" +
              "{a|a|a|a|a|a|A|a}" +
              "{d|d|d|d|d|d|d|D}*"),
    bookends: null
  });

  function getProgressFunction() {
    var ctr = 0;
    return function() {
      ctr += 6;
      if (ctr > 100) {
        return ctr %= 100;
      } else {
        return ctr;
      }
    };
  }
  var bars = [{
    name: "Doodles",
    pattern: "[-|+]*"
  }, {
    name: "Doodles with animation",
    pattern: "{-|+}*"
  }, {
    name: "Kirby",
    pattern: "_*{<|^|(|v}{(|(|>|(}'{o|-|o|.}'{<|)|)|)}{)|^|>|v}"
  }, {
    name: "Kitty",
    patterns: [
      "=(^-^)=",
      "{_|\\\\}(u_u)"
    ]
  }, {
    name: "Nyan cat",
    patterns: [
      "{-|_}*,------,  ",
      "{_|-}*|   /\\\\_/\\\\",
      "{-|_}*|__( ^ .^)",
      "{_|-}* {{\"| }}\"{{ |\"}} {{\"| }}\"{{ |\"}}  "
    ]
  }, {
    name: "Uniform animation",
    pattern: "{{/|\\\\}}*"
  }, {
    name: "Ode to Star Trek II",
    pattern: "KH{{A|a}}*N!"
  }, {
    name: "Pulse going forward",
    pattern: "{_|\\\\|/|_}*"
  }, {
    name: "Pulse going backward",
    pattern: "{_|/|\\\\|_}+"
  }, {
    name: "Multi-line bar",
    patterns: ["{{/|\\\\}}*", "{{\\\\|/}}*"]
  }, {
    name: "American flag",
    patterns: [
      "{*| }*#*",
      "{ |*}* *",
      "{*| }*#*",
      "{ |*}* *",
      "{*| }*#*",
      "[  ]*",
      "[##]*",
      "[  ]*",
      "[##]*"
    ]
  }];

  var placeBar = function(div, obj, prepend, enableSave) {
    var which = obj.patterns ? "multi" : "single";
    var id = which + "Bar" + ("" + Math.random()).substr(2);
    (prepend ? div.prepend : div.append).call(div,
        "<div id=\"" + id + "\" class=\"" + which + " bar-set\">" +
          "<div class=\"title\"></div>" +
          "<div class=\"pattern\"></div>" +
          "<div class=\"buttons\">" +
            (enableSave ? "<div class=\"save\">Save</div>" : "") +
            "<div class=\"close\">Close</div>" +
          "</div>" +
          "<div class=\"bar live-bar\"></div>" +
          "<div class=\"bar stalled-bar\"></div>" +
        "</div>");
    $("#" + id + " .title").html(obj.name);
    $("#" + id + " .pattern").html(
        obj.pattern ? obj.pattern : obj.patterns.join("<br>"));
    if (enableSave) {
      $("#" + id + " .save").click(function() {
        // Insert this thing.
        placeBar($("#savedBars"), obj, true);
      });
    }
    $("#" + id + " .close").click(function() {
      $("#" + id).remove();
    });
    $("#" + id + " .live-bar").nyanBar({
      charSize: charSize,
      pattern: obj.pattern,
      patterns: obj.patterns,
      progressFunction: getProgressFunction(),
      showProgress: true
    });
    $("#" + id + " .stalled-bar").nyanBar({
      charSize: charSize,
      pattern: obj.pattern,
      patterns: obj.patterns,
      progressFunction: function() { return 50; },
      showProgress: true
    });
  };

  var div = $("#singleBars");
  var charSize = 50;
  for (var i = 0; i < bars.length; ++i) {
    placeBar(div, bars[i]);
  }

  // Enable custom progress bar input from the textarea.
  $("#text").keyup(function(e) {
    var id = "id" + ("" + Math.random()).substr(2);
    var patterns = $(this).val().split(/\n/);
    console.log(patterns);
    try {
      var leDiv = $("#customBars");
      leDiv.empty();
      placeBar(leDiv, {
        name: "Your custom progress bar",
        patterns: patterns
      }, false, true);
    } catch (e) {
      // Keep the last valid thing.
      return;
    }
  });
});
