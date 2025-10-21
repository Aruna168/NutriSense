async function apiPost(path, body) {
  const res = await fetch(`/api${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  return res.json();
}

document.addEventListener('DOMContentLoaded', () => {
  const profileForm = document.getElementById('profileForm');
  if (profileForm) {
    profileForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(profileForm).entries());
      try {
        const result = await apiPost('/recommend', data);
        if (result.error) throw new Error(result.error);
        sessionStorage.setItem('targets', JSON.stringify(result.targets));
        sessionStorage.setItem('recommendations', JSON.stringify(result.recommendations));
        window.location.href = '/results';
      } catch (err) {
        document.getElementById('formError').textContent = err.message;
      }
    });
  }

  const feedbackForm = document.getElementById('feedbackForm');
  if (feedbackForm) {
    feedbackForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(feedbackForm).entries());
      const res = await apiPost('/submit_feedback', data);
      const el = document.getElementById('feedbackMsg');
      el.textContent = res.message || res.error || 'Done';
    });
  }
});


