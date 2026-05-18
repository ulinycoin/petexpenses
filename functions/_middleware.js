// Redirect www to non-www canonical domain at the edge
export async function onRequest(context) {
  const url = new URL(context.request.url);

  if (url.hostname === 'www.petexpenses.com') {
    return Response.redirect(
      `https://petexpenses.com${url.pathname}${url.search}`,
      301
    );
  }

  return await context.next();
}
