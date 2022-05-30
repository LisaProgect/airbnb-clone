window.addEventListener("DOMContentLoaded", (event) => {
  const langSelect = document.getElementById("js-lang");
  langSelect.addEventListener("change", (e) => {
    const form = document.getElementById("form_lang");
    form.submit();
  });
});
