document.addEventListener('DOMContentLoaded', function() {
    const follow = document.querySelector('#btfrd');
    const followed = document.querySelector('#pidt').value;
    const flrCount = document.querySelector('#follower');
    const flingCount = document.querySelector('#following');

    follow.addEventListener('click', function() {
        if (follow.innerText == "Follow") {
            fetch(`/profile/${followed}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        follow: true
                    })
                })
                .then(response => response.json())
                .then(data => {
                    flrCount.textContent = `Followers: ${data.follower}`;
                    flingCount.textContent = `Following: ${data.following}`;
                    follow.innerText = "Unfollow";
                })
        } else {
            fetch(`/profile/${followed}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        follow: false
                    })
                })
                .then(response => response.json())
                .then(data => {
                    // unlike.style.display = data.isliked ? "inline-block" : "none";
                    flrCount.textContent = `Followers: ${data.follower}`;
                    flingCount.textContent = `Following: ${data.following}`;
                    follow.innerText = "Follow";
                })
        }
    });
})
