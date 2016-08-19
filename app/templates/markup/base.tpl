<!DOCTYPE html>
<html lang="de">
    <head>
        <meta charset="utf-8">
        <title>{title} – {section_title}</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
        <link href="{root_path}/static/css/style.css" type="text/css" rel="stylesheet">
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
    {flash_info}
       <div class="container-fluid">
            <div class="row">
                <h1 class="col-md-12">{title} – {section_title}</h1>
                <div class="col-md-12">
                   <ul class="nav nav-tabs">
                     {navigation_items}
                   </ul>
                </div>
                <div class="col-md-12">
                   {searchfield}
                   {content}
                </div>
            </div>
        </div>        
    </body>
</html>
