document.addEventListener('DOMContentLoaded', function () {
    function attachSortHandlers() {
        const sortButtons = document.querySelectorAll('.sort-btn');

        sortButtons.forEach(function (button) {
            const newButton = button.cloneNode(true);
            button.parentNode.replaceChild(newButton, button);

            newButton.addEventListener('click', function () {
                const sortBy = this.getAttribute('data-sort-by');
                const currentUrl = new URL(window.location);
                const currentSortDirection =
                    currentUrl.searchParams.get('sort_direction') === 'asc' ? 'desc' : 'asc';

                currentUrl.searchParams.set('sort_by', sortBy);
                currentUrl.searchParams.set('sort_direction', currentSortDirection);
                window.location.href = currentUrl.toString();
            });
        });
    }

    attachSortHandlers();
});