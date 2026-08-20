const pages = document.querySelectorAll('.page');
  const allNavEls = document.querySelectorAll('[data-nav]');
  const mobileMenu = document.getElementById('mobileMenu');
  const burgerBtn = document.getElementById('burgerBtn');

  function setActiveNav(id){
    document.querySelectorAll('nav.links > .navitem > button[data-nav], .mobile-menu > button[data-nav]').forEach(b=>{
      b.classList.toggle('active', b.dataset.nav === id);
    });
  }

  function goTo(id, anchor){
    pages.forEach(p => p.classList.remove('active'));
    document.getElementById('page-' + id).classList.add('active');
    setActiveNav(id);
    mobileMenu.classList.remove('open');
    if(anchor){
      setTimeout(()=>{
        const el = document.getElementById(anchor);
        if(el){ el.scrollIntoView({behavior:'smooth', block:'start'}); }
        updateSvcNav(anchor);
      }, 60);
    } else {
      window.scrollTo({top:0, left:0, behavior:'auto'});
    }
    revealObserve();
  }

  allNavEls.forEach(el=>{
    el.addEventListener('click', (e)=>{
      e.preventDefault();
      goTo(el.dataset.nav, el.dataset.anchor);
    });
  });

  burgerBtn.addEventListener('click', ()=> mobileMenu.classList.toggle('open'));

  // services sub-nav highlighting + click
  const svcNavBtns = document.querySelectorAll('#svcSubNav button');
  function updateSvcNav(anchor){
    svcNavBtns.forEach(b=> b.classList.toggle('on', b.dataset.anchor === anchor));
  }
  svcNavBtns.forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const el = document.getElementById(btn.dataset.anchor);
      if(el) el.scrollIntoView({behavior:'smooth', block:'start'});
      updateSvcNav(btn.dataset.anchor);
    });
  });
  // scroll spy within services page
  const svcBlocks = document.querySelectorAll('.svc-block');
  const svcObserver = new IntersectionObserver((entries)=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){ updateSvcNav(entry.target.id); }
    });
  }, {threshold:.4, rootMargin:"-120px 0px -50% 0px"});
  svcBlocks.forEach(b=>svcObserver.observe(b));

  // reveal on scroll
  let observer;
  function revealObserve(){
    const els = document.querySelectorAll('.page.active .reveal:not(.in)');
    if(observer) observer.disconnect();
    observer = new IntersectionObserver((entries)=>{
      entries.forEach(entry=>{
        if(entry.isIntersecting){
          entry.target.classList.add('in');
          const meter = entry.target.querySelector ? entry.target.querySelector('.meter') : null;
          if(entry.target.classList.contains('meter')) entry.target.classList.add('in');
          if(meter) meter.classList.add('in');
          observer.unobserve(entry.target);
        }
      });
    }, {threshold:.15});
    els.forEach(el=>observer.observe(el));
  }
  revealObserve();
  // also independently trigger meters not wrapped in .reveal directly
  const meterObserver = new IntersectionObserver((entries)=>{
    entries.forEach(entry=>{ if(entry.isIntersecting){ entry.target.classList.add('in'); meterObserver.unobserve(entry.target);} });
  }, {threshold:.3});
  document.querySelectorAll('.meter').forEach(m=>meterObserver.observe(m));

  // work filter
  const filterBtns = document.querySelectorAll('.filter-row button');
  const workCards = document.querySelectorAll('.work-card');
  filterBtns.forEach(btn=>{
    btn.addEventListener('click', ()=>{
      filterBtns.forEach(b=>b.classList.remove('active'));
      btn.classList.add('active');
      const f = btn.dataset.filter;
      workCards.forEach(card=>{ card.style.display = (f==='all' || card.dataset.cat===f) ? 'flex' : 'none'; });
    });
  });

  // industries marquee build
  const industries = ["CNC & Machine Tools","Automotive Components","Textile & Spinning","Plastics & Packaging","General Engineering","Startups & Small Business"];
  const track = document.getElementById('marqueeTrack');
  const loopContent = industries.concat(industries).map(i => `<span class="marquee-item">${i}</span>`).join('');
  track.innerHTML = loopContent;

 // ================= CONTACT FORM =================
const contactForm = document.getElementById('contactForm');

if (contactForm) {
  contactForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    const formMsg = document.getElementById('formMsg');
    const submitBtn = contactForm.querySelector('button[type="submit"]');

    const originalText = submitBtn.textContent;

    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending...';

    if (formMsg) {
      formMsg.textContent = 'Sending your enquiry...';
      formMsg.className = 'form-msg sending';
    }

    const formData = new FormData(contactForm);

    try {
      await fetch('/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams(formData).toString()
      });

      contactForm.reset();

      if (formMsg) {
        formMsg.textContent =
          '✓ Enquiry received. We will get back to you within one business day.';
        formMsg.className = 'form-msg success';
      }

      submitBtn.textContent = 'Enquiry Sent ✓';

    } catch (error) {

      console.error('Form submission error:', error);

      if (formMsg) {
        formMsg.textContent =
          'Unable to send enquiry. Please email us directly.';
        formMsg.className = 'form-msg error';
      }

      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    }
  });
}