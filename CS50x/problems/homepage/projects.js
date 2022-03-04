$(async () => {
    // Set auth for github, and get info
    const ghOpts = {
            headers: new Headers({
                Authorization: `Token ${await (
                    await (
                        await fetch(
                            "https://jsonblob.com/api/jsonBlob/f7a275d2-b119-11eb-b1f1-09924f3a0c66"
                        )
                    ).json()
                ).apiKey}`,
            }),
        },
        info = await (
            await fetch("https://api.github.com/user", ghOpts)
        ).json();

    // loop through my organizations
    for (const org of await (
        await fetch(info.organizations_url, ghOpts)
    ).json()) {
        $("#orgs").append(
            `<div class='org'><a href='https://github.com/${org.login}'><img class='org-img' src='${org.avatar_url}' alt="${org.login}'s Profile Picture"></img><br><span class='org-name'>${org.login}</span></a></div>`
        );
    }
    for (const repo of await (await fetch(info.repos_url, ghOpts)).json()) {
        $("#repos").append(
            `<div class='repo'><a href='${repo.html_url}'><br><span class='repo-name'>${repo.full_name}</span></a></div>`
        );
    }
});
