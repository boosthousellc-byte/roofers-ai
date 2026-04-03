/* ===== Client Acquisition Funnel — JS ===== */

(function() {
  'use strict';

  /* --- Config --- */
  var API_BASE = window.FUNNEL_API_URL || '';

  /* --- Lead Form Handling --- */
  const leadForm = document.getElementById('lead-form');
  if (leadForm) {
    API_BASE = API_BASE || leadForm.getAttribute('data-api-url') || '';

    leadForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const btn = leadForm.querySelector('.form-submit');
      btn.textContent = 'Submitting...';
      btn.disabled = true;

      const formData = new FormData(leadForm);
      const lead = {};
      formData.forEach(function(value, key) { lead[key] = value; });
      lead.submitted_at = new Date().toISOString();
      lead.status = 'new';

      // Always persist locally so the dashboard works offline too
      var leads = JSON.parse(localStorage.getItem('funnel_leads') || '[]');
      leads.push(lead);
      localStorage.setItem('funnel_leads', JSON.stringify(leads));

      function onSuccess() {
        leadForm.style.display = 'none';
        var success = document.getElementById('form-success');
        if (success) success.style.display = 'block';
        setTimeout(function() {
          var businessName = encodeURIComponent(lead.business_name || '');
          window.location.href = 'thank-you.html?business=' + businessName;
        }, 1500);
      }

      // POST to backend API; fall back to local-only on network error
      if (API_BASE) {
        fetch(API_BASE + '/api/leads', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(lead),
        })
          .then(function(res) {
            if (!res.ok) { throw new Error('HTTP ' + res.status); }
            return res.json();
          })
          .then(onSuccess)
          .catch(function() {
            // Backend unreachable — still show success (lead is in localStorage)
            onSuccess();
          });
      } else {
        // No API configured — use localStorage only
        setTimeout(onSuccess, 600);
      }
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

  /* --- Lead Dashboard --- */
  var leadList = document.getElementById('lead-list');

  function renderLeads(leads) {
    if (!leadList) return;
    if (leads.length === 0) {
      leadList.innerHTML = '<p style="color:#64748b;font-size:14px;padding:20px">No leads yet. Share your audit landing page to start collecting leads.</p>';
    } else {
      var html = '<table class="budget-table"><thead><tr><th>Business</th><th>Name</th><th>Email</th><th>Step</th><th>Score</th><th>Status</th></tr></thead><tbody>';
      leads.forEach(function(l) {
        var stepLabel = 'Step ' + (l.sequence_step || '0') + '/7';
        var score = l.lead_score || '0';
        var statusClass = l.status === 'converted' ? 'badge-converted' :
                          l.status === 'sequence_complete' ? 'badge-complete' : '';
        html += '<tr>' +
          '<td>' + escapeHtml(l.business_name || '-') + '</td>' +
          '<td>' + escapeHtml((l.first_name || '') + ' ' + (l.last_name || '')) + '</td>' +
          '<td>' + escapeHtml(l.email || '-') + '</td>' +
          '<td><span style="font-size:12px;background:#e0f2fe;color:#0369a1;padding:2px 8px;border-radius:4px">' + stepLabel + '</span></td>' +
          '<td><strong>' + escapeHtml(score) + '</strong></td>' +
          '<td><span class="badge ' + statusClass + '">' + escapeHtml(l.status || 'new') + '</span></td>' +
          '</tr>';
      });
      html += '</tbody></table>';
      leadList.innerHTML = html;
    }

    // Update stat counters
    var totalLeadsEl = document.getElementById('stat-total-leads');
    if (totalLeadsEl) totalLeadsEl.textContent = leads.length;
  }

  // Try API first, fall back to localStorage
  if (leadList) {
    if (API_BASE) {
      fetch(API_BASE + '/api/leads')
        .then(function(res) { return res.json(); })
        .then(function(leads) { renderLeads(leads); })
        .catch(function() {
          // Fallback to localStorage
          var leads = JSON.parse(localStorage.getItem('funnel_leads') || '[]');
          renderLeads(leads);
        });
    } else {
      var leads = JSON.parse(localStorage.getItem('funnel_leads') || '[]');
      renderLeads(leads);
    }
  }

  /* --- Automation Stats Dashboard --- */
  var autoStats = document.getElementById('auto-stats');
  if (autoStats && API_BASE) {
    fetch(API_BASE + '/api/automations/stats')
      .then(function(res) { return res.json(); })
      .then(function(stats) {
        setStatText('stat-active', stats.active_sequences || 0);
        setStatText('stat-completed', stats.by_status ? (stats.by_status.sequence_complete || 0) : 0);
        setStatText('stat-converted', stats.by_status ? (stats.by_status.converted || 0) : 0);
        setStatText('stat-avg-score', stats.avg_lead_score || 0);
        setStatText('stat-emails-today', stats.emails_sent_today || 0);
        setStatText('stat-sms-today', stats.sms_sent_today || 0);

        // Render step breakdown
        var breakdown = document.getElementById('step-breakdown');
        if (breakdown && stats.by_step) {
          var stepNames = {
            '0': 'New', '1': 'Confirmed', '2': 'Value Add',
            '3': 'Social Proof', '4': 'Paid Offer', '5': 'Objection',
            '6': 'Urgency', '7': 'Breakup'
          };
          var html = '';
          for (var step = 0; step <= 7; step++) {
            var count = stats.by_step[String(step)] || 0;
            var bg = count > 0 ? '#dbeafe' : '#f1f5f9';
            var color = count > 0 ? '#1d4ed8' : '#94a3b8';
            html += '<span style="background:' + bg + ';color:' + color + ';border-radius:8px;padding:8px 16px;font-size:13px;font-weight:600">';
            html += (stepNames[String(step)] || 'Step ' + step) + ': ' + count;
            html += '</span>';
          }
          breakdown.innerHTML = html;
        }
      })
      .catch(function() {
        // Stats not available — set placeholders
        setStatText('stat-active', 'N/A');
        setStatText('stat-completed', 'N/A');
        setStatText('stat-converted', 'N/A');
        setStatText('stat-avg-score', 'N/A');
        setStatText('stat-emails-today', 'N/A');
        setStatText('stat-sms-today', 'N/A');
      });
  }

  /* --- Automation Activity Log --- */
  var autoLog = document.getElementById('auto-log');
  if (autoLog && API_BASE) {
    fetch(API_BASE + '/api/automations/log?limit=15')
      .then(function(res) { return res.json(); })
      .then(function(entries) {
        if (!entries.length) {
          autoLog.innerHTML = '<p style="color:#64748b;font-size:14px">No automation activity yet. Leads will be automatically emailed and texted as they progress through the funnel.</p>';
          return;
        }
        var html = '<table class="budget-table"><thead><tr><th>Time</th><th>Lead</th><th>Event</th><th>Details</th></tr></thead><tbody>';
        entries.reverse().forEach(function(e) {
          var time = e.timestamp ? new Date(e.timestamp).toLocaleString() : '-';
          var icon = e.event_type === 'email_sent' ? '&#9993;' :
                     e.event_type === 'sms_sent' ? '&#128241;' :
                     e.event_type === 'score_updated' ? '&#9733;' :
                     e.event_type === 'sequence_complete' ? '&#10003;' : '&#8226;';
          html += '<tr>' +
            '<td style="font-size:12px;white-space:nowrap">' + time + '</td>' +
            '<td>#' + escapeHtml(e.lead_id || '-') + '</td>' +
            '<td>' + icon + ' ' + escapeHtml(e.event_type || '-') + '</td>' +
            '<td style="font-size:13px;color:#64748b">' + escapeHtml(e.details || '') + '</td>' +
            '</tr>';
        });
        html += '</tbody></table>';
        autoLog.innerHTML = html;
      })
      .catch(function() {
        autoLog.innerHTML = '<p style="color:#64748b;font-size:14px">Connect to the API to see automation activity. Set FUNNEL_API_URL in your environment.</p>';
      });
  } else if (autoLog) {
    autoLog.innerHTML = '<p style="color:#64748b;font-size:14px">Set FUNNEL_API_URL to enable live automation tracking.</p>';
  }

  /* --- Helpers --- */
  function setStatText(id, value) {
    var el = document.getElementById(id);
    if (el) el.textContent = value;
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

})();
