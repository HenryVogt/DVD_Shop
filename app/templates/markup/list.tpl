<h2 class="lead">Seite {page} von {pages_count}</h2>
<form action="{root_path}/{section_path}{query_path}" method="POST">
    <table class="table table-striped">
        <thead>
            {list_head}
        </thead>
        <tbody>
            {list_rows}
        </tbody>
    </table>
</form>
{pagination}