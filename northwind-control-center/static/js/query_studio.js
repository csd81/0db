document.addEventListener('DOMContentLoaded', function () {
  const editor = document.getElementById('sql-editor');
  const savedPicker = document.getElementById('savedPicker');
  const savedId = document.getElementById('savedQueryId');
  const loadBtn = document.getElementById('loadBtn');
  const clearBtn = document.getElementById('clearBtn');
  const readonlyCheck = document.getElementById('readonlyCheck');

  if (loadBtn && savedPicker) {
    loadBtn.addEventListener('click', function () {
      const opt = savedPicker.selectedOptions[0];
      if (!opt || !opt.value) return;
      editor.value = opt.dataset.text || '';
      savedId.value = opt.value;
      if (readonlyCheck) {
        readonlyCheck.checked = opt.dataset.readonly === '1';
      }
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener('click', function () {
      editor.value = '';
      if (savedPicker) savedPicker.selectedIndex = 0;
      if (savedId) savedId.value = '';
    });
  }
});
