'use strict';


ds.commentPost = (function() {
  // vars

  var init = function() {
    // for each comment, listen for:
    // replies & upvotes
    $('.comment').each(function(i, el) {
      var $comment = $(el);
      // upvote listener
      $comment.find('.comment-vote').unbind().click(function(e) {
        // console.log(this);
        vote(e);
      });
      // reply listener
      $comment.find('.comment-actions').unbind().click(function(e) {
        reply(e);
      });
    });
  };

  var vote = function(e) {
    if (e.target.localName == 'i') {
      var commentVote = e.target.getAttribute('data-vote');
      var ul = e.target.parentNode.parentNode;
      var comment = ul.parentNode;
      var score = comment.getAttribute('data-score');
      var text = ul.querySelector('.comment-score');
      var voteState = ul.getAttribute('data-vote-cast');

      // cast vote
      if (voteState === 'none') {
        if (commentVote === 'upvote') score++;
        else if (commentVote === 'downvote') score--;
      }
      // change vote
      else {
        // reset vote
        if (voteState === commentVote) {
          if (commentVote === 'upvote') score--;
          else if (commentVote === 'downvote') score++;
          commentVote = 'none';
        }
        // change vote
        else if (voteState != commentVote) {
          if (commentVote === 'upvote') score = parseInt(score) + 2;
          else if (commentVote === 'downvote') score -= 2;
        }
      }

      // update the DOM/upload to server
      ul.setAttribute('data-vote-cast', commentVote);
      comment.setAttribute('data-score', score);
      text.innerHTML = score;
    }
  };

  var reply = function(e) {
    var action = e.target.innerHTML;
    if (action === 'reply') {
      // is the user logged in?
      // remove event listener for this one
      e.target.innerHTML = '--------';
      // build reply form
      var $form = $('#reply-form').clone();
          // console.log($form);
          // $form.find('#reply-comment_id').attr('value', e.target.parentNode.parentNode.parentNode.getAttribute('data-id'));
          // console.log($form.find('#reply-comment_id'));
          // console.log(e.target.parentNode.parentNode.parentNode.getAttribute('data-id'));
          // $form.find('#reply-comment_id').val(e.target.parentNode.parentNode.parentNode.getAttribute('data-id'))

      // console.log(e.target.parentNode.parentNode.parentNode);
      // console.log(e.target.parentNode.parentNode.parentNode.getAttribute('data-id'));
      $('#reply-form').clone().insertAfter($(e.target.parentNode));
      console.log('inserted form');
      console.log($(e.target.parentNode.parentNode).find('#reply-comment_id'));
      $(e.target.parentNode.parentNode).find('#reply-comment_id').val(e.target.parentNode.parentNode.parentNode.getAttribute('data-id'))
      // $('#reply-form').clone().insertAfter($(e.target.parentNode));
    } else if (action === 'report') {
      console.log('report');
    }
  };

  var replyForm = function() {
    // this is no longer called
    // we build the form with WTForms and copy that to where need
    var form = document.createElement('form');
        form.className = 'reply-form';
    // var csrf_token = document.createElement('input');
        // csrf_token.id = 'csrf_token';
        // csrf_token.name = 'csrf_token';
        // csrf_token.type = 'hidden';
        // csrf_token.value = $('#csrf_token').val();
    var textarea = document.createElement('textarea');
        textarea.setAttribute('placeholder', 'Enter your reply...');
    var div = document.createElement('div');
        div.className = 'submit-comment';
    var input = document.createElement('input');
        input.setAttribute('type', 'submit');
        input.setAttribute('value', 'Submit');
        div.appendChild(input);
    // form.appendChild(csrf_token);
    form.appendChild(textarea);
    form.appendChild(div);
    return form;
  };

  return {
    init : init
  };
})();

ds.commentPost.init();
