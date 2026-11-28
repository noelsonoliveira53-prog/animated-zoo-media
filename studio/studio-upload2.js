// Studio upload helpers (Nov 16, 2026). Paste into the page at studio.youtube.com/channel/<id>/videos/upload?d=ud after setting SHA to a pushed commit.
// Order: armFile(video) -> REAL click "Select files" -> zfill(file) (title, description, made for kids, arms the thumbnail, reads date/time from the plan)
//        -> zthumb() gives the "Upload file" tile's place in an 800-wide screenshot -> REAL click it -> zsched() (refuses without a thumbnail; Next x3, opens Schedule)
//        -> REAL click the date trigger -> zdate() -> type "Nov 19, 2026" + Enter -> ztime() -> type "7:30 AM" + Enter -> zread() -> REAL click Schedule -> zdone() (reads the confirmation, closes it).
// Never publishes: there is no click on "Public" anywhere in this file.
// FIRST, on the content list: zlive(title) (see below) and `python3 studio/upload_guard.py <file>`: one live video per title, never a second upload of a file that is already up.
window.__SHA = 'PUT_A_PUSHED_COMMIT_SHA_HERE';
window.__q = [];
if (!window.__origClick) {
  window.__origClick = HTMLInputElement.prototype.click;
  HTMLInputElement.prototype.click = function () {
    if (this.type === 'file' && window.__q.length) { const f = window.__q.shift(); const dt = new DataTransfer(); dt.items.add(f); this.files = dt.files; this.dispatchEvent(new Event('change', { bubbles: true })); return; }
    return window.__origClick.call(this);
  };
}
window.__RAW = () => 'https://raw.githubusercontent.com/noelsonoliveira53-prog/animated-zoo-media/' + window.__SHA + '/';
// zlive(title): run it on /videos/upload for long videos AND after navigating to /videos/short for Shorts (the in-page Shorts chip did not switch the list, Nov 19).
// zlive(title): the rows of Studio's content list that carry this title, with their visibility. RUN IT ON THE CONTENT LIST BEFORE ARMING A FILE (owner, Nov 17: never upload a video twice).
// live = rows that are Scheduled or Public. A new video needs live = []. A replacement needs live = [the one old id]; after it, live = [the new id] and the old row reads Private.
window.zlive = (title) => { const norm = x => (x || '').replace(/\s+/g, ' ').trim().toLowerCase().replace(/^old \(replaced\): /, ''); const rows = [...document.querySelectorAll('ytcp-video-row')].map(r => { const a = r.querySelector('a#video-title') || r.querySelector('a[href*="/video/"]'); return { id: ((a && a.href || '').split('/video/')[1] || '').split('/')[0], title: (a && a.innerText || '').trim(), vis: ((r.querySelector('.tablecell-visibility') || {}).innerText || '').replace(/\s+/g, ' ').trim(), date: ((r.querySelector('.tablecell-date') || {}).innerText || '').replace(/\s+/g, ' ').trim() }; });
  const same = rows.filter(r => norm(r.title) === norm(title)); return { rows_read: rows.length, same, live: same.filter(r => /Scheduled|Public|Pending|Processing|Draft/.test(r.vis))   /* a row still processing reads Pending (Nov 19): it is live */.map(r => r.id) }; };
window.armFile = async (path, name, type) => { const r = await fetch(window.__RAW() + path); if (!r.ok) return 'HTTP ' + r.status; const b = await r.blob(); window.__q.push(new File([b], name, { type })); return b.size; };
window.zmeta = async (file) => { const r = await fetch(window.__RAW() + 'studio/' + (file.includes('short') ? 'upload_plan_shorts_zoo.json' : 'upload_plan_3d.json')); const p = await r.json(); const items = Array.isArray(p) ? p : (p.videos || p.items); return items.find(e => e.file === file); };
window.zfill = async (file) => { const m = await window.zmeta(file); const T = m.title, D = m.description; const d = document.querySelector('ytcp-uploads-dialog');
  const set = (sel, t) => { const el = d.querySelector(sel); el.focus(); let ok = document.execCommand('selectAll') && document.execCommand('insertText', false, t); if (!ok || el.innerText.trim() !== t.trim()) { el.textContent = t; el.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'insertText', data: t })); } return el.innerText; };
  const t1 = set('ytcp-video-title #textbox', T); const t2 = set('ytcp-video-description #textbox', D);
  const mfk = d.querySelector('tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_MFK"]'); mfk.click(); await new Promise(r => setTimeout(r, 800));
  const sz = await window.armFile(m.thumb, m.thumb.split('/').pop(), 'image/jpeg');
  return { t1, t2len: t2.length, dlen: D.length, mfk: mfk.getAttribute('aria-checked'), thumbBytes: sz, q: window.__q.length, link: (d.innerText.match(/https:\/\/youtu[^\s]+/) || [])[0], date: m.date, time: m.time, status: m.status }; };
window.zthumb = async () => { const tu = document.querySelector('ytcp-uploads-dialog ytcp-thumbnail-uploader'); tu.scrollIntoView({ block: 'center' }); await new Promise(r => setTimeout(r, 800));
  const b = [...tu.querySelectorAll('*')].find(e => e.children.length === 0 && /Upload file/.test(e.textContent));
  if (!b) return { imgs: [...tu.querySelectorAll('img')].map(i => (i.src || '').slice(0, 22) + ' ' + i.naturalWidth + 'x' + i.naturalHeight), q: window.__q.length };
  const r = b.getBoundingClientRect(); return [Math.round((r.x + r.width / 2) * 800 / innerWidth), Math.round((r.y + r.height / 2) * 800 / innerWidth)]; };   // click about 10 px above this point (the tile's icon)
window.zsched = async () => { const d = document.querySelector('ytcp-uploads-dialog'); const sl = ms => new Promise(r => setTimeout(r, ms));
  const tu = d.querySelector('ytcp-thumbnail-uploader'); const imgs = [...tu.querySelectorAll('img')].map(i => (i.src || '').slice(0, 22) + ' ' + i.naturalWidth + 'x' + i.naturalHeight);
  if (![...tu.querySelectorAll('img')].some(i => /^data:|^blob:|^https:\/\/i9\.ytimg\.com\/vi\/[^/]+\/[a-z]*default\.jpg\?v=/.test(i.src || ''))) return { error: 'no thumbnail set', imgs };   // Nov 21: when the video's upload ends before this call the uploader shows the custom thumbnail from i9.ytimg.com (…default.jpg?v=…), no longer the data: image; LOOK at it in a screenshot
  for (let i = 0; i < 3; i++) { d.querySelector('#next-button').click(); await sl(2000); }
  const ex = d.querySelector('#second-container-expand-button'); if (ex && d.querySelector('#done-button').innerText.trim() !== 'Schedule') ex.click(); await sl(1200);   // a Short's dialog can open with Schedule already expanded: a second click closed it and the button read "Publish" (Nov 16). Never click the button unless it reads Schedule
  const tr = d.querySelector('#datepicker-trigger').getBoundingClientRect();
  return { imgs, date: d.querySelector('#datepicker-trigger').innerText, time: (d.querySelector('ytcp-datetime-picker input') || {}).value, trig: [Math.round((tr.x + tr.width / 2) * 800 / innerWidth), Math.round((tr.y + tr.height / 2) * 800 / innerWidth)] }; };
window.zdate = () => { const di = [...document.querySelectorAll('input')].filter(i => /202\d/.test(i.value)); if (di[0]) { di[0].focus(); di[0].select(); } return { n: di.length, v: di[0] && di[0].value, active: document.activeElement === di[0] }; };
window.ztime = () => { const d = document.querySelector('ytcp-uploads-dialog'); const ti = d.querySelector('ytcp-datetime-picker input'); ti.focus(); ti.select(); return { date: d.querySelector('#datepicker-trigger').innerText, time: ti.value, active: document.activeElement === ti }; };
window.zread = () => { const d = document.querySelector('ytcp-uploads-dialog'); const b = d.querySelector('#done-button'); const r = b.getBoundingClientRect(); return { date: d.querySelector('#datepicker-trigger').innerText, time: d.querySelector('ytcp-datetime-picker input').value, header: (d.querySelector('.progress-label') || {}).innerText, btn: b.innerText.trim(), btnAt: [Math.round((r.x + r.width / 2) * 800 / innerWidth), Math.round((r.y + r.height / 2) * 800 / innerWidth)] }; };   // click only when btn reads "Schedule"
window.zdone = () => { const s = [...document.querySelectorAll('ytcp-video-share-dialog, tp-yt-paper-dialog, ytcp-dialog')].filter(x => /Video processing|Video scheduled/.test(x.innerText))[0]; const t = s ? s.innerText.slice(0, 260) : [...document.querySelectorAll('tp-yt-paper-dialog')].filter(x => x.offsetParent).map(x => x.innerText.slice(0, 200)); const c = s && s.querySelector('#close-button, ytcp-button#close-button'); if (c) c.click(); return t; };
'ready';
