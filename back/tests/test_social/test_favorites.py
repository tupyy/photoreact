def test_favorites_post(self):
    """
    Description: Test both POST and DELETE favorite API
    API: /album/{}/favorites
    Method: POST / DELETE
    Date: 19/08/2019
    User: cosmin
    Expected return code: 200
    Expected values:
    """
    self.login(username='user', password='pass')
    client = self.get_client()
    response = client.post('/album/{}/favorites/'.format(self.album.id))
    self.assertEqual(response.status_code, 200)
    self.assertTrue(self.user in self.album.favorites.all())

    # test delete favorites
    response = client.delete('/album/{}/favorites/'.format(self.album.id))
    self.assertEqual(response.status_code, 200)
    self.assertFalse(self.user in self.album.favorites.all())
