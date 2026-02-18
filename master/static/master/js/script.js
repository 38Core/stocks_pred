document.addEventListener('DOMContentLoaded', function () {
    
    // -------------------------
    // 変数を定義
    // -------------------------
    const icons = document.querySelectorAll('.mag-icon');                       // 縦3点アイコン
    
    // 取得した全アイコンにイベントを設定
    icons.forEach(function(icon) {
        // アイコンがクリックされたときの処理
        icon.addEventListener('click', function(e) {
            // クリックイベントが親要素に伝播するのを防ぐ
            e.stopPropagation();

            // クリックされたアイコンの各要素「menu-icon」を取得
            const wrapper = this.closest('.menu-icon');                         // 縦3点アイコン
            const menu = wrapper.querySelector('.menu-list');                   // カンパニーメニュー

            // 現在クリックしたメニュー以外を閉じる
            document.querySelectorAll('.menu-list').forEach(function(m) {
                if (m !== menu) {
                    m.classList.remove('is-open');
                }
            });
            
            // クリックしたメニューの開閉を切り替える
            menu.classList.toggle('is-open');
        });

    });

    // メニュー以外をクリックした場合、メニューを閉じる
    document.addEventListener('click', function() {
        // 全てのメニューを閉じる
        document.querySelectorAll('.menu-list').forEach(function(m) {
            m.classList.remove('is-open');
        });
    });

});

  