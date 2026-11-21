// Runs inside studio.youtube.com (upload dialog open, ?d=ud). Two phases:
//   arm(url, name)  -> fetch the MP4 from GitHub raw and intercept the next file picker
//   fill(meta)      -> title, description, made-for-kids, visibility, publish
window.zoo = {
  async arm(url, name) {
    const blob = await (await fetch(url)).blob();
    window.__zooFile = new File([blob], name, { type: 'video/mp4' });
    if (!window.__origClick) {
      window.__origClick = HTMLInputElement.prototype.click;
      HTMLInputElement.prototype.click = function () {
        if (this.type === 'file' && window.__zooFile) {
          const dt = new DataTransfer(); dt.items.add(window.__zooFile); window.__zooFile = null;
          this.files = dt.files;
          this.dispatchEvent(new Event('change', { bubbles: true }));
          return;
        }
        return window.__origClick.call(this);
      };
    }
    return blob.size;
  },
  async fill(m) {
    const sl = ms => new Promise(r => setTimeout(r, ms));
    const d = document.querySelector('ytcp-uploads-dialog');
    for (let i = 0; i < 30 && !d.querySelector('ytcp-video-title #textbox'); i++) await sl(1000);
    const set = (sel, t) => { const el = d.querySelector(sel); el.focus(); document.execCommand('selectAll'); document.execCommand('insertText', false, t); el.dispatchEvent(new Event('input', { bubbles: true })); };
    set('ytcp-video-title #textbox', m.title);
    set('ytcp-video-description #textbox', m.description);
    d.querySelector('tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_MFK"]').click();
    await sl(800);
    for (let i = 0; i < 3; i++) { d.querySelector('#next-button').click(); await sl(1500); }
    d.querySelector('tp-yt-paper-radio-button[name="' + (m.visibility || 'PUBLIC') + '"]').click();
    await sl(800);
    d.querySelector('#done-button').click();
    for (let i = 0; i < 20; i++) {
      await sl(1500);
      const s = document.querySelector('ytcp-video-share-dialog');
      const link = s && (s.innerText.match(/https:\/\/youtu[^\s]+/) || [])[0];
      if (link) return link;
    }
    return 'no share dialog yet: ' + (document.querySelector('ytcp-uploads-dialog')?.innerText || '').slice(0, 200);
  }
};
'zoo ready';
