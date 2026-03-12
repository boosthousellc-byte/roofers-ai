/* ===== Client Acquisition Funnel — JS ===== */

(function() {
  'use strict';

  /* --- Lead Form Handling --- */
  const leadForm = document.getElementById('lead-form');
  if (leadForm) {
    leadForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const btn = leadForm.querySelector('.form-submit');
      const originalText = btn.textContent;
      btn.textContent = 'Submitting...';
      btn.disabled = true;

      const formData = new FormData(leadForm);
      const lead = {};
      formData.forEach(function(value, key) { lead[key] = value; });

      // Store lead locally
      var leads = JSON.parse(localStorage.getItem('funnel_leads') || '[]');
      lead.submitted_at = new Date().toISOString();
      lead.status = 'new';
      leads.push(lead);
      localStorage.setItem('funnel_leads', JSON.stringify(leads));

      // Simulate submission delay then show success
      setTimeout(function() {
        leadForm.style.display = 'none';
        var success = document.getElementById('form-success');
        if (success) success.style.display = 'block';

        // Redirect to thank-you after brief pause
        setTimeout(function() {
          var businessName = encodeURIComponent(lead.business_name || '');
          window.location.href = 'thank-you.html?business=' + businessName;
        }, 1500);
      }, 800);
    });
  }

  /* --- Template Tab Switching --- */
  var tabs = document.querySelectorAll('.template-tab');
  var sections = document.querySelectorAll('.template-section');

  tabs.forEach(function(tab) {
    tab.addEventListener('click', function() {
      var target = this.getAttribute('data-target');

      tabs.forEach(function(t) { t.classList.remove('active'); });
      this.classList.add('active');

      sections.forEach(function(s) {
        if (target === 'all' || s.getAttribute('data-section') === target) {
          s.style.display = '';
        } else {
          s.style.display = 'none';
        }
      });
    });
  });

  /* --- Copy to Clipboard --- */
  document.querySelectorAll('.copy-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var block = this.closest('.template-block');
      var text = block.querySelector('.template-text');
      if (!text) return;

      // Get raw text, replacing placeholder spans with bracket notation
      var content = text.innerText || text.textContent;

      navigator.clipboard.writeText(content).then(function() {
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(function() {
          btn.textContent = 'Copy';
          btn.classList.remove('copied');
        }, 2000);
      });
    });
  });

  /* --- Collapsible Template Blocks --- */
  document.querySelectorAll('.template-block-header').forEach(function(header) {
    header.addEventListener('click', function(e) {
      if (e.target.classList.contains('copy-btn')) return;
      var body = this.nextElementSibling;
      if (body && body.classList.contains('template-block-body')) {
        body.style.display = body.style.display === 'none' ? '' : 'none';
      }
    });
  });

  /* --- Lead Dashboard (localStorage) --- */
  var leadList = document.getElementById('lead-list');
  if (leadList) {
    var leads = JSON.parse(localStorage.getItem('funnel_leads') || '[]');
    if (leads.length === 0) {
      leadList.innerHTML = '<p style="color:#64748b;font-size:14px;padding:20px">No leads yet. Share your audit landing page to start collecting leads.</p>';
    } else {
      var html = '<table class="budget-table"><thead><tr><th>Business</th><th>Name</th><th>Email</th><th>Submitted</th><th>Status</th></tr></thead><tbody>';
      leads.forEach(function(l, i) {
        var date = new Date(l.submitted_at).toLocaleDateString();
        html += '<tr>' +
          '<td>' + escapeHtml(l.business_name || '-') + '</td>' +
          '<td>' + escapeHtml((l.first_name || '') + ' ' + (l.last_name || '')) + '</td>' +
          '<td>' + escapeHtml(l.email || '-') + '</td>' +
          '<td>' + date + '</td>' +
          '<td><span class="badge">' + escapeHtml(l.status || 'new') + '</span></td>' +
          '</tr>';
      });
      html += '</tbody></table>';
      leadList.innerHTML = html;
    }

    // Update stat counters
    var totalLeadsEl = document.getElementById('stat-total-leads');
    if (totalLeadsEl) totalLeadsEl.textContent = leads.length;
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

})();
