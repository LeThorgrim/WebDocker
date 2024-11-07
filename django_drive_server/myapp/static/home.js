document.addEventListener('DOMContentLoaded', function() {
    const menuItems = document.querySelectorAll('.sidebar a');
    const contentSections = document.querySelectorAll('.content-section');

    // Masquer toutes les sections de contenu
    contentSections.forEach(section => section.style.display = 'none');

    // Afficher la section de contenu "accueil"
    const accueilSection = document.getElementById('content-home');
    if (accueilSection) {
        accueilSection.style.display = 'block';
    }

    menuItems.forEach(item => {
        item.addEventListener('click', function(event) {
            event.preventDefault();

            // Masquer toutes les sections de contenu
            contentSections.forEach(section => section.style.display = 'none');

            // Afficher la section de contenu correspondante
            const contentId = 'content-' + item.id;
            document.getElementById(contentId).style.display = 'block';
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const folders = document.querySelectorAll('.folder');

    folders.forEach(folder => {
        folder.addEventListener('click', function() {
            alert(`Ouvrir le dossier: ${folder.querySelector('span').textContent}`);
            // Ajoutez ici la logique pour charger le contenu du dossier cliqué
        });
    });
});



//drag and drop
function drag(event) {
    event.dataTransfer.setData("file_id", event.target.getAttribute("data-file-id"));
}

function allowDrop(event) {
    event.preventDefault();
}

function drop(event) {
    event.preventDefault();
    const fileId = event.dataTransfer.getData("file_id");
    const folderId = event.target.closest('.folder').getAttribute("data-folder-id");

    // Vérifiez si fileId et folderId sont définis correctement
    console.log("Dragging File ID:", fileId, "to Folder ID:", folderId);

    if (fileId && folderId) {
        fetch("{% url 'move_file_to_folder' %}", {
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `file_id=${fileId}&folder_id=${folderId}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Mettre à jour l'interface après le succès
                const fileElement = document.querySelector(`[data-file-id="${fileId}"]`);
                const targetFolder = document.querySelector(`[data-folder-id="${folderId}"] .folder-contents`);

                if (fileElement && targetFolder) {
                    targetFolder.appendChild(fileElement);
                }
            } else {
                console.error(data.message);
            }
        })
        .catch(error => console.error('Erreur:', error));
    } else {
        console.error("fileId ou folderId est manquant.");
    }
}



document.querySelectorAll('.folder').forEach(folder => {
    folder.addEventListener('dragenter', () => folder.classList.add('drag-over'));
    folder.addEventListener('dragleave', () => folder.classList.remove('drag-over'));
});

