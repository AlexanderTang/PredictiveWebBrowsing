// ==UserScript==
// @name        URL Stream Handler
// @namespace   be.kuleuven.cs.dtai
// @description Send visited urls to local server and show most likely links.
// @version     1
// @grant       GM_xmlhttpRequest
// @run-at      document-end
// ==/UserScript==

try {
  var toppage = (window.top == window.self);
  if (!toppage) {
    return;
  }

  var url = window.location.href;

  var send = function(data, onload) {
    data.ts = (new Date()).toISOString();
    data_string = JSON.stringify(data);
    GM_xmlhttpRequest({
      method: "POST",
      url: "http://localhost:8000",
      data: data_string,
      headers: {
        "Content-Type": "application/json",
        "Content-Length": data.length
      },
      onerror: function(error) {
        console.log('Calling urlStreamHandler failed', error);
      },
      onload: onload
    });
  };

  // Associate a click event with all links
  var addClickEvent = function(element) {
    if (element.dataset.dtaitracked) {
      return;
    }
    element.dataset.dtaitracked = true;
    element.addEventListener('click', function(link) {return function(event) {
      try {
        var href = '';
        if (link.href !== undefined) {
          href = link.href;
        }
        send({
          "action": "click",
          "target": href,
          "url": url,
        });
      } catch (e) {
        console.log('An error occured in a click listener', e);
      }
    };}(element));
  };
  for (var i=0; i<document.links.length; i++) {
    addClickEvent(document.links[i]);
  }
  var observer = new MutationObserver(function(mutations) {
    try {
      mutations.forEach(function(mutation) {
        try {
          var node;
          for (var i=0; i<mutation.addedNodes.length; i++) {
            node = mutation.addedNodes[i];
            if (node.tagName === "A" || node.tagName === "a") {
              addClickEvent(node);
            } else if (node.getElementsByTagName) {
              var atags = node.getElementsByTagName('a');
              for (var aidx=0; aidx<atags.length; aidx++) {
                addClickEvent(atags[aidx]);
              }
            }
          }
        } catch (e) {
          console.log('An error occured processing added nodes', e);
        }
      });
    } catch (e) {
      console.log('An error occured after a mutation change', e);
    }
  });
  observer.observe(document.body, {childList:true, subtree:true});


  // Window events
  // Possible events include hashchange, pageshow, popstate, beforeunload
  window.addEventListener('beforeunload', function(event) {
    send({
      "action": 'beforeunload',
      "url": url
    });
  });

  // Catch any other changes by polling the location
  setInterval(function() {
    try {
      if(location.href !== url) {
        send({
          "action": 'polling',
          "url": location.href,
        });
        url = location.href;
      }
    } catch (e) {
      console.log('An error occured while processing polled change', e);
    }
  }, 500);

  // Send current page load and react to result
  var html = '';
  if (document.body) {
    html = document.body.innerHTML;
  }
  send({
    "action": "load",
    "url": url,
    "top": toppage,
    "html": html
  }, function(response) {
    try {
      data = JSON.parse(response.response);
      // TODO: Do something (e.g. show a top bar with the final link of the
      //       suspected sequence)
      var best_guess = data.guesses[0][0];
      
      var myDiv = document.createElement("div");
      //document.getElementsByTagName('div')[0].innerHTML += "OUR PREDICTION: "+best_guess.link("http://"+best_guess);

      //myDiv.setAttribute('href',"http://"+best_guess);
      //myDiv.innerHTML = "OUR PREDICTION: "+best_guess;
      myDiv.innerHTML = "OUR PREDICTION: "+best_guess.link("http://"+best_guess);
      document.getElementsByTagName('div')[0].appendChild(myDiv);
      
     // var d = document.getElementById('yourDivId');
     // d.style.position = "absolute";
    //  d.style.left = x_pos+'px';
    //  d.style.top = y_pos+'px';
      
      var l = document.links;
      for (var i=0; i<l.length; i++) {
        // As a simple example, we highlight the link with the highest
        // probability.
        if (l[i].href == "http://"+best_guess) {
          l[i].style["background-color"]="yellow";
        }
      }
    } catch (e) {
      console.log('An error occured while processing the guesses', e);
    }
  });
} catch (e) {
  console.log('An error occured', e);
}

