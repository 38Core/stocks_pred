// =====================================================
// ① DOM読み込み後に実行（メニュー・検索UI制御）
// =====================================================
document.addEventListener('DOMContentLoaded', () => {

  // -------------------------
  // 要素取得
  // -------------------------
  const menuBtn    = document.querySelector('.menu-button');
  const menu       = document.querySelector('.slide-menu');
  const searchBtn  = document.querySelector('.pc-menu-search');
  const search     = document.querySelector('.search-input-field');
  const headerLeft = document.querySelector('.header-left-group');

  // =====================================================
  // ② ハンバーガーメニューの開閉制御
  //    ・メニュー開閉
  //    ・検索バーとの排他制御
  // =====================================================
  if (menuBtn && menu) {

    // --- メニューボタンクリック ---
    menuBtn.addEventListener('click', (ev) => {
      ev.stopPropagation();

      const isOpen = menu.classList.toggle('is-open');

      // メニューを開いたとき
      if (isOpen) {

        // 検索バーが開いていたら閉じる
        if (search.classList.contains('is-active')) {
          search.classList.remove('is-active');
        }

        // 検索バーを背面に回して操作不可にする
        if (search) {
          search.style.zIndex = '0';
          search.style.pointerEvents = 'none';
        }

      // メニューを閉じたとき
      } else {
        // 検索バーの表示状態を元に戻す
        if (search) {
          search.style.zIndex = '';
          search.style.pointerEvents = '';
        }
      }
    });

    // --- メニュー外クリックで閉じる ---
    document.addEventListener('click', (ev) => {
      const isClickInsideMenu   = menu.contains(ev.target);
      const isClickOnMenuButton = menuBtn.contains(ev.target);

      if (
        menu.classList.contains('is-open') &&
        !isClickInsideMenu &&
        !isClickOnMenuButton
      ) {
        menu.classList.remove('is-open');

        // 検索バーの状態を元に戻す
        if (search) {
          search.style.zIndex = '';
          search.style.pointerEvents = '';
        }
      }
    });
  }

  // =====================================================
  // ③ PC用 検索バー表示制御
  //    ※ モバイルでは動作させない
  // =====================================================
  if (searchBtn && search) {

    // --- 検索ボタンクリック ---
    searchBtn.addEventListener('click', (ev) => {
      if (window.innerWidth <= 768) return; // モバイル除外
      ev.stopPropagation();

      const isActive = search.classList.toggle('is-active');

      if (isActive) {
        // 左ヘッダーを非表示
        if (headerLeft) {
          headerLeft.style.opacity = '0';
          headerLeft.style.pointerEvents = 'none';
        }
        // 入力欄にフォーカス
        search.querySelector('.search-input').focus();
      } else {
        // 左ヘッダーを復帰
        if (headerLeft) {
          headerLeft.style.opacity = '1';
          headerLeft.style.pointerEvents = 'auto';
        }
      }
    });

    // --- 検索バー外クリックで閉じる ---
    document.addEventListener('click', (ev) => {
      if (window.innerWidth <= 768) return;

      const isClickInsideSearch = search.contains(ev.target);
      const isClickOnSearchBtn  = searchBtn.contains(ev.target);
      const isSearchOpen        = search.classList.contains('is-active');

      if (isSearchOpen && !isClickInsideSearch && !isClickOnSearchBtn) {
        if (headerLeft) {
          headerLeft.style.opacity = '1';
          headerLeft.style.pointerEvents = 'auto';
        }
        search.classList.remove('is-active');
      }
    });
  }
});


