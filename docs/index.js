document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImg');

    // Open modal when any gallery image is clicked
    const galleryImages = document.querySelectorAll('.gallery img');
    galleryImages.forEach(img => {
        img.addEventListener('click', function () {
            modalImg.src = this.src;
            modalImg.alt = this.alt;
            modal.style.display = 'flex';
        });
    });

    // Close modal when clicking outside the image or pressing Escape
    modal.addEventListener('click', function (e) {
        // If the click is on the modal background (not the image), close
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Also close on Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.style.display === 'flex') {
            modal.style.display = 'none';
        }
    });
});
