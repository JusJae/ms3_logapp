# Testing

## Validations

[CSS Validation](/docs/testing/validation/css-validation.png)

## Responsiveness & Compatibility

[Testing Matrix](/docs/testing/testing-matrix.png)

## Performance & Accessibility

[Lighthouse Report - Desktop](/docs/testing/performance/lighthouse-desktop-home.png)

[Lighthouse Report - Mobile](/docs/testing/performance/lighthouse-mobile-home.png)

## User Stories

| User Story ID | User Story Description | Screenshot | Status |
|---------------|------------------------|------------|--------|
| 1.1           | As a new user, I want to register for an account so that I can access the product log app. | ![Register](/docs/testing/user-story_images/us-register.png) | Met |
| 1.2           | As a registered user, I want to log in to the application so that I can manage my product list. | ![Login](/docs/testing/user-story_images/us-login.png) | Met |
| 1.3           | As a registered user, I want to reset my password in case I forget it. | ![Reset Password](/docs/testing/user-story_images/us-edit-profile.png) | Partially Met |
| 2.1           | As a user, I want to add a new product to my list, including its image, so that I can keep track of my products. | ![Add Product](/docs/testing/user-story_images/us-add-product.png) | Met |
| 2.2           | As a user, I want to view all my products in a list or grid view so that I can easily navigate through them. | ![View Products](/docs/testing/user-story_images/us-products.png) | Met |
| 2.3           | As a user, I want to update the details of a product, including changing its image, to keep my product information current. | ![Update Product](/docs/testing/user-story_images/us-edit-product.png) | Met |
| 2.4           | As a user, I want to delete a product from my list when I no longer need it. | ![Delete Product](/docs/testing/user-story_images/us-products.png) | Met |
| 3.1           | As a user, I want to search for a product by its name to quickly find specific products. | ![Search Product](/docs/testing/user-story_images/us-search-products.png) | Met |
| 3.2           | As a user, I want to filter products by categories to view products of a specific type. | ![Filter Products](/docs/testing/user-story_images/us-categories.png) | Met |
| 3.3           | As a user, I want to sort products by the date they were added to see recent additions first. | ![Sort Products](/docs/testing/user-story_images/us-search-products.png) | Not Met |
| 4.1           | As a user, I want a responsive layout so that I can access the application effectively on both desktop and mobile devices. | ![Responsive Layout](/docs/testing/user-story_images/us-mobile-view.jpeg) | Met |
| 4.2           | As a user, I want a fixed bottom footer with relevant links and information. | ![Footer](/docs/testing/user-story_images/us-footer.png) | Met |
| 4.3           | As a user, I want a navigation menu to quickly move between different sections of the application. | ![Navigation Menu](/docs/testing/user-story_images/us-mobile-menu.png) | Met |
| 5.1           | As a user, I want to view products in paginated lists so that I don’t get overwhelmed with too much data at once and the app loads faster. | ![Pagination](link_to_image) | Not Met |
| 6.1           | As a user with visual impairments, I want the application to be screen-reader friendly so that I can navigate and use the app effectively. | ![Accessibility](link_to_image) | Partially Met |
| 6.2           | As a user with motor impairments, I want to navigate the application using keyboard shortcuts. | ![Keyboard Navigation](link_to_image) | Met |
| 7.1           | As a user, I want my uploaded product images to be stored securely and load fast. | ![Cloud Storage](link_to_image) | Met |
| 7.2           | As a user, I want the application to only accept valid image files to ensure consistency and safety. | ![Media Management](link_to_image) | Partially Met |
| 8.1           | As a user, I want to receive clear error messages when something goes wrong so that I understand what happened and how to proceed. | ![Error Handling](link_to_image) | Partially Met |
| 8.2           | As a user, I want to receive feedback when my actions (like adding a product) are successful. | ![Feedback](/docs/testing/user-story_images/us-feedback.png) | Met |

## Bugs

These are some of the bugs that I had to overcome whist in development of this project.

- Adjusting the positioning of elements in the navbar.
- Handling search functionality and error redirection when the user is not logged in.
- Modifying the user profile editing functionality to prevent duplicate usernames and to update passwords securely.
- Displaying the current password in an edit profile form but storing it hashed in the database.
- Fixing the login form redirection and flashed message display.
- Fixing linting errors specifically (E501) in Python code.
