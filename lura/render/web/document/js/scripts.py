channelActivatorScript='''
    
     new QWebChannel(
        qt.webChannelTransport, 
        function(channel) {
            var db = channel.objects.db;
            window.db = db;
            });
     '''

annotatorScript='''

	 var app = new annotator.App(); 

	 app.include(annotator.ui.main, {
		editorExtensions: [annotator.ui.tags.editorExtension],
		viewerExtensions: [annotator.ui.tags.viewerExtension]
	 });

     app.include(annotator.storage.http, {
         prefix: 'http://127.0.0.1:5000'
         });

    var updateAnnotation = function() {
        return {
            beforeAnnotationCreated: function(annotation) {
                var url= window.location.href.replace(/#.*$/, '').replace(/\?.*$/, '');
                annotation.url=url;
                }
            }
            }

                
    app.include(updateAnnotation)

	app.start();

    '''

loadScript='''

    var url= window.location.href.replace(/#.*$/, '').replace(/\?.*$/, '');
    app.annotations.load({'filePath':url})

    '''

test='''
    link=document.createElement('link')
    link.href='https://recogito.github.io/recogito-js/recogito.min.css';
    link.rel='stylesheet';

    js=document.createElement('script')
    js.src='https://recogito.github.io/recogito-js/recogito.min.js';
    '''

recogitoActivatorScript='''

    (function() {
      var r = Recogito.init({
        content: document.body
      });

      // Add an event handler  
      r.on('createAnnotation', function(annotation) { 
        window.db.annotationCreated(annotation);
        });
    })();
    '''


annotatorActivatorScript='''

	 var app = new annotator.App(); 
	 app.include(annotator.ui.main, {
		editorExtensions: [annotator.ui.tags.editorExtension],
		viewerExtensions: [annotator.ui.tags.viewerExtension]
	 });

     app.include(annotator.storage.noop);


    function actBeforeAnnotationCreated() {
        return {
            beforeAnnotationCreated: function (annotation) {
                db.beforeAnnotationCreated(annotation);
            }
        };
    }

    function actAnnotationCreated() {
        return {
            annotationCreated: function (annotation) {
                db.annotationCreated(annotation);
            }
        };
    }

    function actAnnotationUpdated() {
        return {
            annotationUpdated: function (annotation) {
                db.annotationUpdated(annotation);
            }
        };
    }

    function actAnnotationDeleted() {
        return {
            annotationDeleted: function (annotation) {
                db.annotationDeleted(annotation);
            }
        };
    }

    function actAnnotationsLoaded() {
        return {
            annotationsLoaded: function (annotations) {
                db.annotationsLoaded(annotations);
            }
        };
    }

    app.include(actBeforeAnnotationCreated)
    app.include(actAnnotationCreated)
    app.include(actAnnotationUpdated)
    app.include(actAnnotationDeleted)
    app.include(actAnnotationsLoaded)
	app.start();
	'''
loadAnnotationsScript=''' '''

getAuthor='''
    var author = "";
    var info = document.getElementsByTagName('META');
    for (var i=0;i<info.length;i++) {
      if (info[i].getAttribute('NAME').toLowerCase()=='author') {
          author = info[i].getAttribute('CONTENT');
            }
        }
    '''
