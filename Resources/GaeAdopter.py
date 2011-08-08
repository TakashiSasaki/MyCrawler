'''
@author: Takashi SASAKI
@contact: takashi316@gmail.com
@license: Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
@copyright: Takashi SASAKI, 2011
'''
from __future__ import with_statement
from google.appengine.api import apiproxy_stub_map  
class GaeAdopter(object):
    def __init__(self, app_id="app", datastore_path="app.db", blobstore_path="app.blob"):
        self.app_id = app_id
        import os
        os.environ['APPLICATION_ID'] = app_id
        self.config = { "datastore_path": datastore_path,
                         "blobstore_path" : blobstore_path }
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
        self._RegisterDatastore()
        self._RegisterBlobstore()

    def _RegisterDatastore(self):
        from google.appengine.datastore import datastore_sqlite_stub
        self.datastore_path = self.config['datastore_path']
        require_indexes = self.config.get('require_indexes', False)
        trusted = self.config.get('trusted', False)

        datastore = datastore_sqlite_stub.DatastoreSqliteStub(
            self.app_id, self.datastore_path,
            require_indexes=require_indexes, trusted=trusted)
        apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', datastore)

    def _RegisterBlobstore(self):
        from google.appengine.api.blobstore import file_blob_storage
        from google.appengine.api.blobstore import blobstore_stub
        from google.appengine.api.files import file_service_stub
        blobstore_path = self.config['blobstore_path']
        blob_storage = file_blob_storage.FileBlobStorage(blobstore_path, self.app_id)
        apiproxy_stub_map.apiproxy.RegisterStub('blobstore',
            blobstore_stub.BlobstoreServiceStub(blob_storage))

        apiproxy_stub_map.apiproxy.RegisterStub('file',
            file_service_stub.FileServiceStub(blob_storage))

def _main():
    from google.appengine.ext import db
    class Greeting(db.Model):
        author = db.UserProperty()
        content = db.StringProperty(multiline=True)
        date = db.DateTimeProperty(auto_now_add=True)
        
    gae_adoptor = GaeAdoptor()

    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    
    greeting = Greeting()
    greeting.content = "content content content"
    greeting.put()

    logging.debug("getting out models")
    greetings = db.GqlQuery("SELECT * FROM Greeting ORDER BY date DESC LIMIT 10")
    for greeting in greetings:
        if greeting.author:
            print greeting.author.nickname()
        else:
            print greeting.content
            print greeting.date

    logging.debug("creating a file")
    from google.appengine.api import files
    file_name = files.blobstore.create(mime_type='application/octet-stream')
    with files.open(file_name, 'a') as f:
        f.write('data')
    files.finalize(file_name)
    blob_key = files.blobstore.get_blob_key(file_name)
    return "GaeAdopter._main() finished."

if __name__ == "__main__":
    _main()
    import sys, trace
    #tracer = trace.Trace(ignoredirs=[sys.prefix, sys.exec_prefix])
    tracer = trace.Trace()
    tracer.run("_main()")
    results = tracer.results()
    results.write_results(True, coverdir="tracer_results")
