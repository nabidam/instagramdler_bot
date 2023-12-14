from instaloader import instaloader, Profile, Post

# Get instance
L = instaloader.Instaloader()
profile = Profile.from_username(L.context, '___naa____')
# print(profile)
# print("{} follows these profiles:".format(profile.username))
# for followee in profile.get_followees():
#     print(followee.

# for post in profile.get_posts():
#     L.download_post(post, target=profile.username)
L.interactive_login("___naa____")
post = Post.from_shortcode(L.context, "CmUi3RMOqVa")
L.download_post(post, target=profile.username)
